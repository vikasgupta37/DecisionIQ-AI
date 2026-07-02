from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.core.exceptions import DecisionIQException, EntityNotFoundException
from backend.app.crud.dashboard import dashboard_repository
from backend.app.crud.dataset import dataset_repository
from backend.app.models.dataset import DatasetStatus
from backend.app.models.processing_report import ProcessingReport
from backend.app.models.user import User
from backend.app.schemas.processing import (
    ProcessingReportResponse,
    ProcessingResponse,
)
from backend.app.services.data_processor import data_processor_service, PROCESSABLE_EXTENSIONS
from backend.app.services.storage import get_storage_service

router = APIRouter()


@router.post("/{dataset_id}", response_model=ProcessingResponse, status_code=200)
def process_dataset(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    dataset_id: int,
) -> Any:
    """
    Triggers the data processing pipeline for a dataset.
    Runs validation, cleaning, normalization, and statistics computation.
    Updates dataset status to 'completed' or 'failed'.
    """
    # 1. Fetch dataset
    dataset = dataset_repository.get(db, dataset_id=dataset_id)
    if not dataset:
        raise EntityNotFoundException("Dataset", dataset_id)

    # 2. Check if the file type is processable
    if dataset.file_type not in PROCESSABLE_EXTENSIONS:
        raise DecisionIQException(
            message=f"File type '{dataset.file_type}' cannot be processed. Supported: {list(PROCESSABLE_EXTENSIONS)}",
            status_code=400,
            code="UNPROCESSABLE_TYPE",
        )

    # 3. Mark as processing
    dataset_repository.update_status(db, dataset_id, DatasetStatus.PROCESSING)

    try:
        # 4. Read file content from storage
        storage = get_storage_service()
        file_path = storage.get_file_path(dataset.gcs_uri or "")
        with open(file_path, "rb") as f:
            content = f.read()

        # 5. Run pipeline
        if dataset.file_type == "csv":
            result = data_processor_service.process_csv(content)
        elif dataset.file_type == "json":
            result = data_processor_service.process_json(content)
        elif dataset.file_type in ("xlsx", "xls"):
            # Convert Excel to CSV-like rows via openpyxl and process
            result = _process_excel(content)
        else:
            raise DecisionIQException(
                message=f"No processor for type '{dataset.file_type}'",
                status_code=400,
                code="NO_PROCESSOR",
            )

        if not result.success:
            dataset_repository.update_status(db, dataset_id, DatasetStatus.FAILED)
            raise DecisionIQException(
                message=f"Processing failed: {result.error}",
                status_code=500,
                code="PROCESSING_FAILED",
            )

        # 6. Persist the processing report
        report = ProcessingReport(
            dataset_id=dataset_id,
            quality_report=result.quality_report.model_dump() if result.quality_report else {},
            column_stats={cs.name: cs.model_dump() for cs in result.column_stats},
            original_row_count=result.original_row_count,
            cleaned_row_count=result.cleaned_row_count,
            duplicates_removed=result.duplicates_removed,
            nulls_filled=result.nulls_filled,
            log="\n".join(result.log_messages),
        )
        db.add(report)

        # 7. Mark as completed and update row count
        dataset.status = DatasetStatus.COMPLETED
        dataset.row_count = result.cleaned_row_count
        db.commit()

        # 8. Log activity
        dashboard_repository.log_activity(
            db,
            user_id=current_user.id,
            action="data_processing",
            details=f"Processed '{dataset.name}': {result.original_row_count} → {result.cleaned_row_count} rows ({result.duplicates_removed} duplicates removed)",
        )

        return ProcessingResponse(
            dataset_id=dataset_id,
            status="completed",
            original_row_count=result.original_row_count,
            cleaned_row_count=result.cleaned_row_count,
            duplicates_removed=result.duplicates_removed,
            nulls_filled=result.nulls_filled,
            quality_report=result.quality_report,
            column_stats=result.column_stats,
            log="\n".join(result.log_messages),
        )

    except DecisionIQException:
        raise
    except Exception as e:
        dataset_repository.update_status(db, dataset_id, DatasetStatus.FAILED)
        raise DecisionIQException(
            message=f"Processing failed: {str(e)}",
            status_code=500,
            code="PROCESSING_FAILED",
        )


@router.get("/{dataset_id}/report", response_model=ProcessingReportResponse)
def get_processing_report(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    dataset_id: int,
) -> Any:
    """Retrieves the persisted processing report for a dataset."""
    from sqlalchemy import select
    stmt = select(ProcessingReport).where(ProcessingReport.dataset_id == dataset_id)
    report = db.scalars(stmt).first()
    if not report:
        raise EntityNotFoundException("ProcessingReport", dataset_id)
    return ProcessingReportResponse.model_validate(report)


def _process_excel(content: bytes):
    """Helper to process Excel files by converting to CSV-like tabular format."""
    import io
    import openpyxl
    from backend.app.services.data_processor import data_processor_service

    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb.active
    if not ws:
        from backend.app.services.data_processor import ProcessingResult
        return ProcessingResult(success=True, original_row_count=0, cleaned_row_count=0)

    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append([str(cell) if cell is not None else "" for cell in row])
    wb.close()

    if not rows:
        from backend.app.services.data_processor import ProcessingResult
        return ProcessingResult(success=True, original_row_count=0, cleaned_row_count=0)

    # Convert to CSV bytes and process
    output = io.StringIO()
    writer = __import__("csv").writer(output)
    for row in rows:
        writer.writerow(row)
    csv_bytes = output.getvalue().encode("utf-8")
    return data_processor_service.process_csv(csv_bytes)
