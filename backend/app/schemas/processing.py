from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class ColumnStats(BaseModel):
    """Per-column statistics computed during data processing."""
    name: str
    dtype: str
    total_count: int
    null_count: int
    unique_count: int
    null_percentage: float
    min: Optional[Any] = None
    max: Optional[Any] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    top_values: Optional[List[Any]] = None


class DataQualityReport(BaseModel):
    """Overall data quality metrics for a processed dataset."""
    completeness: float       # Percentage of non-null values (0-100)
    duplicate_ratio: float    # Percentage of duplicate rows (0-100)
    null_ratio: float         # Percentage of null values across all cells (0-100)
    total_cells: int
    total_nulls: int
    total_duplicates: int


class ProcessingResponse(BaseModel):
    """Full processing result returned after pipeline execution."""
    dataset_id: int
    status: str
    original_row_count: int
    cleaned_row_count: int
    duplicates_removed: int
    nulls_filled: int
    quality_report: DataQualityReport
    column_stats: List[ColumnStats]
    log: Optional[str] = None


class ProcessingReportResponse(BaseModel):
    """Persisted processing report from database."""
    id: int
    dataset_id: int
    quality_report: Dict[str, Any]
    column_stats: Dict[str, Any]
    original_row_count: int
    cleaned_row_count: int
    duplicates_removed: int
    nulls_filled: int
    log: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
