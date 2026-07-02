from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
from backend.app.models.dataset import DatasetStatus


class DatasetResponse(BaseModel):
    """Full dataset record response."""
    id: int
    name: str
    file_type: str
    file_size: int
    status: DatasetStatus
    row_count: Optional[int] = None
    gcs_uri: Optional[str] = None
    bq_table_id: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetListResponse(BaseModel):
    """Paginated list of datasets."""
    datasets: List[DatasetResponse]
    total: int


class UploadMetadata(BaseModel):
    """Metadata extracted from the uploaded file."""
    row_count: Optional[int] = None
    column_names: Optional[List[str]] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    extra: Dict[str, Any] = {}


class UploadResponse(BaseModel):
    """Response returned after a successful file upload."""
    dataset: DatasetResponse
    metadata: UploadMetadata
    message: str = "File uploaded successfully"
