from typing import Any, List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.crud.dashboard import dashboard_repository
from backend.app.crud.dataset import dataset_repository
from backend.app.models.user import User
from backend.app.schemas.dataset import (
    DatasetListResponse,
    DatasetResponse,
    UploadMetadata,
    UploadResponse,
)
from backend.app.services.file_processor import file_processor_service
from backend.app.services.storage import get_storage_service

router = APIRouter()


@router.post("", response_model=UploadResponse, status_code=201)
def upload_file(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    file: UploadFile = File(..., description="File to upload (CSV, Excel, PDF, JSON, TXT, DOCX)"),
) -> Any:
    """
    Upload a file to the platform.
    Validates file type and size, stores the file, extracts metadata,
    creates a Dataset record, and logs the activity.
    """
    # 1. Validate file type and size
    file_processor_service.validate_file(file)

    # 2. Extract metadata before storage
    metadata = file_processor_service.extract_metadata(file)

    # 3. Store file
    storage = get_storage_service()
    storage_uri = storage.save_file(file, directory=str(current_user.id))

    # 4. Create dataset record
    dataset = dataset_repository.create(
        db,
        name=metadata.filename,
        file_type=metadata.file_type,
        file_size=metadata.file_size,
        user_id=current_user.id,
        row_count=metadata.row_count,
        gcs_uri=storage_uri,
    )

    # 5. Log the upload activity
    dashboard_repository.log_activity(
        db,
        user_id=current_user.id,
        action="file_upload",
        details=f"Uploaded {metadata.filename} ({metadata.file_type}, {metadata.file_size} bytes)",
    )

    return UploadResponse(
        dataset=DatasetResponse.model_validate(dataset),
        metadata=UploadMetadata(
            row_count=metadata.row_count,
            column_names=metadata.column_names,
            page_count=metadata.page_count,
            word_count=metadata.word_count,
            extra=metadata.extra,
        ),
        message=f"File '{metadata.filename}' uploaded successfully.",
    )


@router.get("", response_model=DatasetListResponse)
def list_datasets(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    limit: int = 50,
    offset: int = 0,
) -> Any:
    """
    Lists all datasets uploaded by the current user.
    """
    datasets = dataset_repository.get_by_user(
        db, user_id=current_user.id, limit=limit, offset=offset
    )
    return DatasetListResponse(
        datasets=[DatasetResponse.model_validate(d) for d in datasets],
        total=len(datasets),
    )


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    dataset_id: int,
) -> Any:
    """
    Retrieves a single dataset by its ID.
    """
    dataset = dataset_repository.get(db, dataset_id=dataset_id)
    if not dataset:
        raise EntityNotFoundException("Dataset", dataset_id)
    return DatasetResponse.model_validate(dataset)
