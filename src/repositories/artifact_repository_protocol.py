from typing import List, Protocol
from src.domain.artifact import Artifact

class ArtifactRepositoryProtocol(Protocol):

    def add_artifact(self, artifact: Artifact) -> str:
        ...

    def get_artifact_by_id(self, artifact_id: str) -> Artifact:
        ...

    def get_artifact_by_accession_number(self, accession_number: str) -> Artifact:
        ...

    def get_artifacts_by_museum(self, museum_id: str) -> List[Artifact]:
        ...

    def get_parent_artifacts(self, artifact_id: str) -> List[Artifact]:
        ...

    def remove_artifact(self, artifact_id: str, updated_fields_dict: dict) -> Artifact:
        ...
    
    def remove_artifact(self, artifact_id: str) -> str:
        ...

    
