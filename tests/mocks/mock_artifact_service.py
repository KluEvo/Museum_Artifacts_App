from src.repositories.artifact_repository_protocol import ArtifactRepositoryProtocol
from src.domain.artifact import Artifact
from src.domain.museum import Museum
from src.repositories.museum_repository_protocol import MuseumRepositoryProtocol
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List
import logging
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)
logger = logging.getLogger(__name__)


class MockArtifactService:
    def __init__(
        self
    ):
        self.artifacts = [
            Artifact(         
                artifact_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                name="Mock Artifact",
                discovery_date=datetime(2000, 1, 2),
                estimated_value=100000,
                accession_number="MOCK12345",
                museum_id="bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                parent_artifact=None,
            ),
            Artifact(
                artifact_id="aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa",
                name="Mock Artifact 2",
                discovery_date=datetime(2000, 1, 2),
                estimated_value=100000,
                accession_number="MOCK67890",
                museum_id="bbbbbbbb-bbbb-aaaa-aaaa-aaaaaaaaaaaa",
                parent_artifact=None,
            ),
            Artifact(
                artifact_id="aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa",
                name="Mock Artifact 3",
                discovery_date=datetime(2000, 1, 2),
                estimated_value=100000,
                accession_number="MOCK54321",
                museum_id="bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                parent_artifact=None,
            ),
        ]
        self.museums = [
            Museum(         
                museum_id="bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    name = "Test Museum 1",
                    location = "Test Location 1",
                    contact_email = "test1@email.com",
            ),
            Museum(
                museum_id="bbbbbbbb-bbbb-aaaa-aaaa-aaaaaaaaaaaa",
                    name = "Test Museum 2",
                    location = "Test Location 2",
                    contact_email = "test2@email.com",
            ),
            Museum(
                museum_id="bbbbbbbb-cccc-aaaa-aaaa-aaaaaaaaaaaa",
                    name = "Test Museum 2",
                    location = "Test Location 2",
                    contact_email = "test2@email.com",
            ),
        ]

    def get_all_artifacts(self) -> List[Artifact]:
        return self.artifacts
        
    def get_artifact_count(self) -> int:
        try:
            return len(self.artifacts)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving all artifacts."
            ) from e

    def add_artifact(self, artifact: Artifact) -> str:
        if not isinstance(artifact, Artifact):
            raise ValidationException("Invalid Artifact object provided.")

        try:
            return artifact.artifact_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while adding artifact."
            ) from e

    def remove_artifact(self, artifact_id: str) -> str:
        if not isinstance(artifact_id, str):
            raise ValidationException("Artifact ID must be a string.")

        try:
            for arti in self.artifacts:
                if artifact_id == arti.artifact_id:
                    return artifact_id
            raise NotFoundException(f"Artifact with id {artifact_id} not found.")    
            
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while removing artifact."
            ) from e

    def find_artifacts_by_name(self, query: str) -> List[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Query must be a string.")

        try:
            print("test")
            for arti in self.artifacts:
                if query == arti.name:
                    return arti.artifact_id
                
            raise NotFoundException(f"No artifacts found with name '{query}'.")
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching artifacts by name."
            ) from e

    def find_artifacts_by_accession_number(self, query: str) -> List[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Query must be a string.")

        try:
            for arti in self.artifacts:
                if query == arti.accession_number:
                    return arti.artifact_id
            raise NotFoundException(f"No artifacts found with accession number '{query}'.")
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching artifacts by accession number."
            ) from e

    def find_artifacts_by_museum(self, query: str) -> list[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Museum ID must be a string.")

        try:
            m_id = ""
            for museum in self.museums:
                if query == museum.museum_id:
                    m_id = museum.museum_id
            
            if m_id == "":
                raise NotFoundException(f"Museum with id {query} not found.")
            
            artifacts = []
            for arti in self.artifacts:
                if query == arti.museum_id:
                    artifacts.append(arti)
            if not artifacts:
                raise NotFoundException(f"No artifacts found for museum id {query}.")
            return artifacts
        
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching artifacts by museum."
            ) from e

    def find_parent_artifact(self, query: str) -> list[Artifact]:
        if not isinstance(query, str):
            raise ValidationException("Query must be a string.")

        try:
            for arti in self.artifacts:
                if query == arti.parent_artifact:
                    return arti.parent_artifact
            raise NotFoundException(f"No parent artifact found for id {query}.")
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while searching parent artifact."
            ) from e

    def find_artifact_by_id(self, artifact_id: str) -> Artifact:
        if not isinstance(artifact_id, str):
            raise ValidationException(f"Artifact ID must be a string, got {artifact_id}")

        try:
            for arti in self.artifacts:
                if artifact_id == arti.artifact_id:
                    return arti.artifact_id
            raise NotFoundException(f"Artifact with id {artifact_id} not found.")
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving artifact by ID."
            ) from e

    def update_artifact(self, artifact_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(artifact_id, str):
            raise ValidationException("Artifact ID must be a string.")

        if not isinstance(updated_fields_dict, dict):
            raise ValidationException("Updated fields must be a dictionary.")

        try:
            for arti in self.artifacts:
                if artifact_id == arti.artifact_id:
                    return arti.artifact_id
            raise NotFoundException(f"Artifact with id {artifact_id} not found.")
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while updating artifact."
            ) from e
