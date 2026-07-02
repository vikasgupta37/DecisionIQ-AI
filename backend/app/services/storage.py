import os
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from fastapi import UploadFile


class StorageService(ABC):
    """
    Abstract storage service defining the interface for file persistence.
    Implementations can target local disk, Google Cloud Storage, S3, etc.
    """

    @abstractmethod
    def save_file(self, file: UploadFile, directory: str) -> str:
        """
        Saves an uploaded file and returns the storage URI or path.
        """
        ...

    @abstractmethod
    def get_file_path(self, uri: str) -> str:
        """
        Resolves a storage URI to a readable file path.
        """
        ...

    @abstractmethod
    def delete_file(self, uri: str) -> bool:
        """
        Deletes a file from storage. Returns True if successful.
        """
        ...


class LocalStorageService(StorageService):
    """
    Local filesystem storage implementation for development and testing.
    Files are stored under a configurable base directory with UUID-prefixed
    filenames to prevent collisions.
    """

    def __init__(self, base_dir: str = "uploads"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file: UploadFile, directory: str = "") -> str:
        """
        Saves an uploaded file to the local filesystem.
        Returns the relative path as the storage URI.
        """
        target_dir = self.base_dir / directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Generate a unique filename to prevent collisions
        file_ext = os.path.splitext(file.filename or "file")[1]
        unique_name = f"{uuid.uuid4().hex}{file_ext}"
        file_path = target_dir / unique_name

        # Read and write file content
        content = file.file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Reset file pointer for potential re-reads
        file.file.seek(0)

        return str(file_path)

    def get_file_path(self, uri: str) -> str:
        """
        Returns the absolute path for a local storage URI.
        """
        return str(Path(uri).resolve())

    def delete_file(self, uri: str) -> bool:
        """
        Deletes a file from local storage.
        """
        path = Path(uri)
        if path.exists():
            path.unlink()
            return True
        return False


def get_storage_service() -> StorageService:
    """
    Factory function returning the active storage service implementation.
    Swap this to GCSStorageService for production deployments.
    """
    return LocalStorageService(base_dir="uploads")
