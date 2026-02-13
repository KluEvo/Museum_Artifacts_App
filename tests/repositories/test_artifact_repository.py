import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.repositories.artifact_repository as artifact_repository
from src.domain.artifact import Artifact
import uuid
from datetime import datetime


@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    Artifact.metadata.create_all(engine)
    yield engine
    Artifact.metadata.drop_all(engine)
@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    artifacts = [
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
            name="Mock Artifact D",
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number="MOCK67890",
            museum_id=uuid.UUID("bbbbbbbb-bbbb-aaaa-aaaa-aaaaaaaaaaaa"),
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
        ),
    ]

    session.add_all(artifacts)
    session.flush()   # ensures IDs are available immediately

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def repo(session):
    return artifact_repository.ArtifactRepository(session)



def test_get_all_artifacts(repo):
    artifacts = repo.get_all_artifacts()
    assert len(artifacts) == 3
    assert artifacts[0].name =='Mock Artifact'
    assert artifacts[2].name =='Mock Artifact D'

def test_add_artifact(repo):
    new_artifact = Artifact(
            artifact_id=uuid.UUID("aaaaaaaa-dddd-aaaa-aaaa-aaaaaaaaaaaa"),
            name='Mock New Artifact',
            discovery_date=datetime(2000, 1, 2),
            estimated_value=100000,
            accession_number='NEWM12345',
            museum_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            parent_artifact=None,

        )
    repo.add_artifact(new_artifact)
    artifacts = repo.get_all_artifacts()
    assert len(artifacts) == 4
    assert artifacts[3].name == 'Mock New Artifact'

def test_find_artifact_by_name(repo):
    result = repo.get_artifacts_by_name("Mock Artifact")
    assert len(result) == 1
    assert result[0].name == "Mock Artifact"

def test_find_multiple_artifacts_by_name(repo):
    result = repo.get_artifacts_by_name("Mock Artifact D")
    assert len(result) == 2
    assert result[0].name == "Mock Artifact D"
    assert result[1].name == "Mock Artifact D"


def test_find_artifact_by_name_failure(repo):
    result = repo.get_artifacts_by_name("Artifact 20")
    assert len(result) == 0

def test_find_artifact_by_id(session):
    repo = artifact_repository.ArtifactRepository(session)
    result = repo.get_artifact_by_id("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    assert result
    assert result.name == "Mock Artifact"

def test_find_artifact_by_id_not_found(session):
    repo = artifact_repository.ArtifactRepository(session)
    result = repo.get_artifact_by_id("aaaaaaaa-ffff-ffff-ffff-aaaaaaaaaaaa")
    assert result is None

def test_remove_artifact(session):
    repo = artifact_repository.ArtifactRepository(session)
    repo.remove_artifact("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    artifacts = repo.get_all_artifacts()
    assert len(artifacts) == 2
    assert artifacts[0].name == "Mock Artifact D"


def test_remove_invalid_artifact(session):
    repo = artifact_repository.ArtifactRepository(session)
    repo.remove_artifact("aaaaaaaa-abcd-aaaa-aaaa-aaaaaaaaaaaa")
    artifacts = repo.get_all_artifacts()
    assert len(artifacts) == 3
    assert artifacts[0].name == "Mock Artifact"
    assert artifacts[1].name == "Mock Artifact D"
    assert artifacts[2].name == "Mock Artifact D"
    
def test_update_artifact(session):
    repo = artifact_repository.ArtifactRepository(session)
    repo.update_artifact("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", {"name": "Updated Artifact 1"})
    artifact = repo.get_artifact_by_id("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    assert artifact.name == "Updated Artifact 1"

def test_update_artifact_invalid_field(session):
    repo = artifact_repository.ArtifactRepository(session)
    with pytest.raises(ValueError):
        # no title field
        repo.update_artifact("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", {"title": "Updated Artifact 1"})


