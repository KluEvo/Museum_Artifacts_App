from src.domain.artifact import Artifact
from typing import List
from datetime import datetime
import uuid

class MockArtifactRepository:

    def add_artifact(self, artifact: Artifact) -> str:
        return 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'

    def get_artifact_by_id(self, artifact_id: str) -> Artifact:
        return Artifact(         
            artifact_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            name="Mock Artifact",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK12345",
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        )

    def get_artifacts_by_accession_number(self, accession_number: str) -> Artifact:
        return Artifact(         
            artifact_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            name="Mock Artifact",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK12345",
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        )

    def get_artifacts_by_name(self, name: str) -> List[Artifact]:
        return [
        Artifact(         
            artifact_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            name="Mock Artifact",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK12345",
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        ),
        Artifact(
            artifact_id=uuid.UUID("aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa"),
            name=name,
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK67890",
            museum_id=uuid.UUID("bbbbbbbb-bbbb-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        ),
        Artifact(
            artifact_id=uuid.UUID("aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"),
            name=name,
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK54321",
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        ),
    ]

    def get_all_artifacts(self) -> List[Artifact]:
        return [
        Artifact(         
            artifact_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            name="Mock Artifact",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK12345",
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        ),
        Artifact(
            artifact_id=uuid.UUID("aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa"),
            name="Mock Artifact 2",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK67890",
            museum_id=uuid.UUID("bbbbbbbb-bbbb-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        ),
        Artifact(
            artifact_id=uuid.UUID("aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"),
            name="Mock Artifact 3",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK54321",
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,
        ),
    ]

    def get_artifacts_by_museum(self, museum_id: str) -> List[Artifact]:
        return [
            Artifact(         
                artifact_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                name="Mock Artifact",
                discovery_date=datetime(2000, 1, 2),
                estimated_value=100000,
                accession_number="MOCK12345",
                museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                parent_artifact=None,
            ),
            Artifact(
                artifact_id=uuid.UUID("aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"),
                name="Mock Artifact D",
                discovery_date=datetime(2000, 1, 2),
                estimated_value=100000,
                accession_number="MOCK54321",
                museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                parent_artifact=None,
            )
        ]

    def get_parent_artifact(self, artifact_id: str) -> List[Artifact]:
        return [
            Artifact(
                artifact_id=uuid.UUID("aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"),
                name="Mock Artifact D",
                discovery_date=datetime(2000, 1, 2),
                estimated_value=100000,
                accession_number="MOCK54321",
                museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                parent_artifact=None,
            )
        ]

    def update_artifact(self, artifact_id: str, updated_fields_dict: dict) -> Artifact:
        return Artifact(
            artifact_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            name=updated_fields_dict.get('name', 'Mock Artifact'),
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number=updated_fields_dict.get('accession_number', 'MOCK12345'),
            museum_id=uuid.UUID(updated_fields_dict.get('museum_id', 'mock_museum_id')),
            parent_artifact=updated_fields_dict.get('parent_artifact_id', None)
        )
    
    def remove_artifact(self, artifact_id: str) -> str:
        if artifact_id in ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa", "aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"]:
            return artifact_id
        return None
