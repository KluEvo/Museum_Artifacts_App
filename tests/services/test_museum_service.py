import pytest

import src.services.museum_service as museum_service
from src.domain.museum import Museum
from tests.mocks.mock_museum_repository import MockMuseumRepository
from src.exceptions import ValidationException


def test_get_all_museums_positive():
    # passes
    repo = MockMuseumRepository()
    svc = museum_service.MuseumService(repo)
    museums = svc.get_all_museums()
    assert len(museums) == 1

def test_add_museum_positive():
    # passes
    #may not get back proper id
    repo = MockMuseumRepository()
    svc = museum_service.MuseumService(repo)
    museum = Museum(
            museum_id = 'mock_id', 
            name = 'test', 
            location = 'test', 
            contact_email = 'test@test.com'
            )
    #pass id?
    id = svc.add_museum(museum)
    assert id == 'mock_id'

def test_get_museum_by_id_positive():
    # passes
    #probably not how this should be
    repo = MockMuseumRepository()
    svc = museum_service.MuseumService(repo)
    id='test'
    museum = svc.get_museum_by_id(id)
    assert museum.name == 'test'

def test_remove_museum_positive():
    repo = MockMuseumRepository()
    svc = museum_service.MuseumService(repo)
    id = svc.remove_museum('mock_id')
    assert id == 'mock_id'


