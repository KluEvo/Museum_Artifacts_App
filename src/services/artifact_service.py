from src.repositories.artifact_repository_protocol import ArtifactRepositoryProtocol
from src.domain.artifact import Artifact
from src.repositories.museum_repository_protocol import MuseumRepositoryProtocol
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)
import logging
logger = logging.getLogger(__name__)


class ArtifactService:
    def __init__(
        self,
        artifact_repo: ArtifactRepositoryProtocol,
        museum_repo: MuseumRepositoryProtocol = None
    ):
        self.artifact_repo = artifact_repo
        self.museum_repo = museum_repo 

    def get_all_artifacts(self) -> List[Artifact]:
        try:
            return self.artifact_repo.get_all_artifacts()
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving all artifacts."
            ) from e
        
    def get_artifact_count(self) -> int:
        try:
            artifacts = self.artifact_repo.get_all_artifacts()
            return len(artifacts)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving all artifacts."
            ) from e

    def add_artifact(self, artifact: Artifact) -> str:
        if not isinstance(artifact, Artifact):
            raise ValidationException("Invalid Artifact object provided.")

        logger.info("Adding artifact %s", artifact.accession_number)

        try:
            return self.artifact_repo.add_artifact(artifact)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while adding artifact."
            ) from e

    def remove_artifact(self, artifact_id: str) -> str:
        if not isinstance(artifact_id, str):
            raise ValidationException("Artifact ID must be a string.")

        logger.info("Removing artifact %s", artifact_id)

        try:
            removed_id = self.artifact_repo.remove_artifact(artifact_id)
            if not removed_id:
                raise NotFoundException(f"Artifact with id {artifact_id} not found.")    
            return removed_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while removing artifact."
            ) from e

    def find_artifacts_by_name(self, query: str) -> List[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Query must be a string.")

        try:
            artifacts = self.artifact_repo.get_artifacts_by_name(query)
            if not artifacts:
                raise NotFoundException(f"No artifacts found with name '{query}'.")
            return artifacts
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching artifacts by name."
            ) from e

    def find_artifacts_by_accession_number(self, query: str) -> List[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Query must be a string.")

        try:
            artifacts = self.artifact_repo.get_artifacts_by_accession_number(query)
            if not artifacts:
                raise NotFoundException(f"No artifacts found with accession number '{query}'.")
            return artifacts
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching artifacts by accession number."
            ) from e

    def find_artifacts_by_museum(self, query: str) -> List[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Museum ID must be a string.")

        try:
            museum = self.museum_repo.get_museum_by_id(query)
            if museum is None:
                raise NotFoundException(f"Museum with id {query} not found.")
            artifacts = self.artifact_repo.get_artifacts_by_museum(query)
            if not artifacts:
                raise NotFoundException(f"No artifacts found for museum id {query}.")
            return artifacts
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching artifacts by museum."
            ) from e

    def find_parent_artifact(self, query: str) -> List[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Query must be a string.")

        try:
            artifacts = self.artifact_repo.get_parent_artifact(query)
            if not artifacts:
                raise NotFoundException(f"No parent artifact found for id {query}.")
            return artifacts
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching parent artifact."
            ) from e

    def find_artifact_by_id(self, artifact_id: str) -> Artifact:
        if not isinstance(artifact_id, str):
            raise ValidationException(f"Artifact ID must be a string, got {artifact_id}")

        try:
            artifact = self.artifact_repo.get_artifact_by_id(artifact_id)
            if artifact is None:
                raise NotFoundException(f"Artifact with id {artifact_id} not found.")
            return artifact
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving artifact by ID."
            ) from e

    def update_artifact(self, artifact_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(artifact_id, str):
            raise ValidationException("Artifact ID must be a string.")

        logger.info("Updating artifact %s", artifact_id)

        if not isinstance(updated_fields_dict, dict):
            raise ValidationException("Updated fields must be a dictionary.")

        try:
            updated_id = self.artifact_repo.update_artifact(artifact_id, updated_fields_dict)
            if not updated_id:
                raise NotFoundException(f"Artifact with id {artifact_id} not found.")
            return updated_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while updating artifact."
            ) from e
