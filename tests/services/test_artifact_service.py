import pytest
import src.services.artifact_service as artifact_service
from tests.mocks.mock_artifact_repository import MockArtifactRepository
from src.exceptions import ValidationException, NotFoundException

def test_get_all_artifacts_positive():
    # passes
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)
    artifacts = svc.get_all_artifacts()
    assert len(artifacts) == 3

def test_get_all_artifacts_negative():
    # passes
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)

    with pytest.raises(ValidationException) as e:
        svc.find_artifacts_by_museum(123)
        assert "Query must be a string" in str(e.value)

def test_add_artifact_positive():
    # passes
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)
    count = svc.get_artifact_count()
    assert count == 3

def test_add_artifact_negative():
    # passes
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)

    with pytest.raises(ValidationException) as e:
        svc.add_artifact("not an artifact hi")  #empty name should fail
        assert "name cannot be empty" in str(e.value)

def test_remove_artifact_positive():
    # passes
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)
    artifact_id = "aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"
    result = svc.remove_artifact(artifact_id)
    assert result == artifact_id

def test_remove_artifact_negative():
    # passes
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)

    with pytest.raises(ValidationException) as e:
        svc.remove_artifact(123)
        assert "artifact id must be a string" in str(e.value)

def test_remove_artifact_not_found_negative():
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)

    with pytest.raises(NotFoundException):
        svc.remove_artifact("nonexistent_id")

def test_find_artifacts_by_museum_negative():
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)

    with pytest.raises(ValidationException) as e:
        svc.find_artifacts_by_museum(456)
        assert "museum id must be a string" in str(e.value)

def test_find_artifact_by_id_negative():
    repo = MockArtifactRepository()
    svc = artifact_service.ArtifactService(repo)

    with pytest.raises(ValidationException) as e:
        svc.find_artifact_by_id(789)
        assert "artifact id must be a string" in str(e.value)