import enum
from datetime import datetime, timezone
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.core.database import Base


class DatasetStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # csv, xlsx, pdf, etc.
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)  # size in bytes
    status: Mapped[DatasetStatus] = mapped_column(
        Enum(DatasetStatus), default=DatasetStatus.PENDING, nullable=False
    )
    row_count: Mapped[int] = mapped_column(Integer, nullable=True)
    gcs_uri: Mapped[str] = mapped_column(String(1024), nullable=True)
    bq_table_id: Mapped[str] = mapped_column(String(1024), nullable=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
