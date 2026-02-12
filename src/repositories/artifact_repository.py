from typing import List
from sqlalchemy.orm import Session
from src.domain.artifact import Artifact
from src.repositories.artifact_repository_protocol import ArtifactRepositoryProtocol

class ArtifactRepository(ArtifactRepositoryProtocol):
    def __init__(self, session : Session):
        self.session = session

    def get_all_artifacts(self) -> List[Artifact]:
        return self.session.query(Artifact).all()

    def add_artifact(self, artifact: Artifact) -> str:
        self.session.add(artifact)
        self.session.commit()
        return str(artifact.artifact_id)
    
    def remove_artifact(self, artifact_id: str) -> str:
        artifacts = self.get_artifact_by_id(artifact_id)
        if len(artifacts) != 1:
            raise ValueError(f"No artifact with id: {artifact_id}")
        artifact = artifacts[0]
        self.session.delete(artifact)
        self.session.commit()
        print("deleted")
        return str(artifact_id)
    
    def get_artifact_by_id(self, artifact_id: str) -> Artifact:
        return self.session.query(Artifact).filter(Artifact.artifact_id == artifact_id).all()

    def get_artifacts_by_accession_number(self, accession_number: str) -> List[Artifact]:
        return self.session.query(Artifact).filter(Artifact.accession_number == accession_number).all()
    
    def get_artifacts_by_name(self, name: str) -> List[Artifact]:
        return self.session.query(Artifact).filter(Artifact.name == name).all()

    def get_artifacts_by_museum(self, museum_id: str) -> List[Artifact]:
        return self.session.query(Artifact).filter(Artifact.museum_id == museum_id).all()

    def get_parent_artifact(self, artifact_id: str) -> List[Artifact]:
        child = self.session.query(Artifact).filter(Artifact.artifact_id == artifact_id).first()
        if not child or not child.parent_id:
            return []
        return self.session.query(Artifact).filter(Artifact.artifact_id == child.parent_artifact_id).all()

    def update_artifact(self, artifact_id: str, updated_fields_dict: dict) -> str:
        artifact_to_update = self.session.query(Artifact).filter(Artifact.artifact_id == artifact_id).first()
        if not artifact_to_update:
            return None 

        allowed_fields = {col.name for col in Artifact.__table__.columns if not col.primary_key}

        for field, value in updated_fields_dict.items(): #validation!
            if field not in allowed_fields:
                raise ValueError(f"Field not updatable: {field}")
            setattr(artifact_to_update, field, value)

        self.session.commit()
        return str(artifact_to_update.artifact_id)
