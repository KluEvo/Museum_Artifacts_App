from src.repositories.artifact_repository_protocol import ArtifactRepositoryProtocol
from src.domain.artifact import Artifact

class ArtifactService:
    def __init__(self, artifact_repo: ArtifactRepositoryProtocol):
        self.artifact_repo = artifact_repo

    def get_all_artifacts(self) -> list[Artifact]:
        return self.artifact_repo.get_all_artifacts()

    def add_artifact(self, artifact: Artifact) -> str:
        return self.artifact_repo.add_artifact(artifact)
    
    def remove_artifact(self, artifact_id: str) -> str:
        return self.artifact_repo.remove_artifact(artifact_id)

    def find_artifact_by_name(self, query: str) -> list[Artifact]:
        if not isinstance(query, str):
            raise ValueError("Expected str, got something else")
        return self.artifact_repo.find_artifact_by_name(query)

    def find_artifact_by_id(self, artifact_id: str) -> Artifact:
        if not isinstance(artifact_id, str):
            raise ValueError("Expected str, got something else")
        return self.artifact_repo.get_artifact_by_id(artifact_id)
    
    def update_artifact(self, artifact_id:str, updated_fields_dict: dict) -> str:
        if not isinstance(artifact_id, str):
            raise TypeError('Expected str, got something else.')
        if not isinstance(updated_fields_dict, dict):
            raise TypeError('Expected a dict, got something else.')
        return self.artifact_repo.update_artifact(artifact_id, updated_fields_dict)
    
