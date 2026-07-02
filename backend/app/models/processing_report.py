from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.core.database import Base


class ProcessingReport(Base):
    __tablename__ = "processing_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dataset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    # Quality metrics stored as JSON
    quality_report: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # Per-column statistics stored as JSON
    column_stats: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # Processing summary
    original_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cleaned_row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duplicates_removed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nulls_filled: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Processing log / error messages
    log: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
