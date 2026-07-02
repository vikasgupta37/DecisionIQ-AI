from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.dataset import Dataset, DatasetStatus


class DatasetRepository:
    """Repository for Dataset CRUD operations using SQLAlchemy 2.0 patterns."""

    def create(
        self,
        db: Session,
        *,
        name: str,
        file_type: str,
        file_size: int,
        user_id: int,
        row_count: Optional[int] = None,
        gcs_uri: Optional[str] = None,
        status: DatasetStatus = DatasetStatus.PENDING,
    ) -> Dataset:
        """Creates a new dataset record."""
        dataset = Dataset(
            name=name,
            file_type=file_type,
            file_size=file_size,
            user_id=user_id,
            row_count=row_count,
            gcs_uri=gcs_uri,
            status=status,
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset

    def get(self, db: Session, dataset_id: int) -> Optional[Dataset]:
        """Retrieves a dataset by its primary key."""
        return db.get(Dataset, dataset_id)

    def get_by_user(
        self, db: Session, user_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dataset]:
        """Retrieves all datasets belonging to a specific user, ordered by newest first."""
        stmt = (
            select(Dataset)
            .where(Dataset.user_id == user_id)
            .order_by(Dataset.created_at.desc(), Dataset.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(db.scalars(stmt).all())

    def list_all(self, db: Session, limit: int = 50, offset: int = 0) -> List[Dataset]:
        """Retrieves all datasets ordered by newest first. Admin use."""
        stmt = (
            select(Dataset)
            .order_by(Dataset.created_at.desc(), Dataset.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(db.scalars(stmt).all())

    def update_status(
        self, db: Session, dataset_id: int, status: DatasetStatus
    ) -> Optional[Dataset]:
        """Updates the processing status of a dataset."""
        dataset = self.get(db, dataset_id)
        if dataset:
            dataset.status = status
            db.commit()
            db.refresh(dataset)
        return dataset


dataset_repository = DatasetRepository()
