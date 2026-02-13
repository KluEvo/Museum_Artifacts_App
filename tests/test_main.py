from fastapi.testclient import TestClient
import pytest
from tests.mocks.mock_artifact_service import MockArtifactService
from src.main import app, get_artifact_service


def override_artifact_service():
    return MockArtifactService()

app.dependency_overrides[get_artifact_service] = override_artifact_service


client = TestClient(app)

def test_get_all_artifacts():
    response = client.get("/artifacts")
    assert response.status_code == 200
    assert response.json() == [
        {'accession_number': 'MOCK12345', 
         'name': 'Mock Artifact', 
         'discovery_date': '2000-01-02T00:00:00', 
         'estimated_value': 100000, 
         'parent_artifact': None, 
         'museum_id': 'bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 
         'artifact_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'}, 
         {'accession_number': 'MOCK67890', 
          'name': 'Mock Artifact 2', 
          'discovery_date': '2000-01-02T00:00:00', 
          'estimated_value': 100000, 
          'parent_artifact': None, 
          'museum_id': 
          'bbbbbbbb-bbbb-aaaa-aaaa-aaaaaaaaaaaa', 
          'artifact_id': 'aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa'}, 
          {'accession_number': 'MOCK54321', 
           'name': 'Mock Artifact 3', 
           'discovery_date': 
           '2000-01-02T00:00:00', 
           'estimated_value': 100000, 
           'parent_artifact': None, 
           'museum_id': 'bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 
           'artifact_id': 'aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa'}]


def test_remove_artifact_name():
    response = client.delete("/artifact?id=aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa")
    assert response.status_code == 200
    assert response.json() == "aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa"


def test_remove_artifact_name_nonexistent():
    artifact_id = "aaaaaaaa-dcba-aaaa-aaaa-aaaaaaaaaaaa"
    response = client.delete(f"/artifact?id={artifact_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Artifact with id {artifact_id} not found."

def test_get_all_artifacts_of_a_museum():
    museum_id = "bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    response = client.get(f"/artifacts/from_museum?id={museum_id}")
    assert response.status_code == 200
    
    assert response.json() == [
        {'accession_number': 'MOCK12345', 
         'name': 'Mock Artifact', 
         'discovery_date': '2000-01-02T00:00:00', 
         'estimated_value': 100000, 
         'parent_artifact': None, 
         'museum_id': 'bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 
         'artifact_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'}, 
          {'accession_number': 'MOCK54321', 
           'name': 'Mock Artifact 3', 
           'discovery_date': 
           '2000-01-02T00:00:00', 
           'estimated_value': 100000, 
           'parent_artifact': None, 
           'museum_id': 'bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 
           'artifact_id': 'aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa'}]
    # assert response.json()["detail"] == f"No Artifact from musuem of id {museum_id}."

def test_get_all_artifacts_of_a_non_existent_museum():
    museum_id = "bbbbbbbb-aaaa-bbbb-aaaa-aaaaaaaaaaaa"
    response = client.get(f"/artifacts/from_museum?id={museum_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Museum with id {museum_id} not found."

def test_get_all_artifacts_of_an_empty_museum():
    museum_id = "bbbbbbbb-cccc-aaaa-aaaa-aaaaaaaaaaaa"
    response = client.get(f"/artifacts/from_museum?id={museum_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"No artifacts found for museum id {museum_id}."
