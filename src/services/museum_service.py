from src.repositories.museum_repository_protocol import MuseumRepositoryProtocol
from src.domain.museum import Museum


class MuseumService:
    def __init__(self, museum_repo: MuseumRepositoryProtocol):
        self.museum_repo = museum_repo

    def add_museum(self, museum: Museum) -> str:
        return self.museum_repo.add_museum(museum)
    
    def get_museum_by_id(self, museum_id: str) -> str:
        if not isinstance(museum_id, str):
            raise TypeError('Expected str, got something else.')
        return self.museum_repo.get_museum_by_id(museum_id)

    def get_all_museums(self) -> str:
        return self.museum_repo.get_all_museums()

    def update_museum(self, museum_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(museum_id, str):
            raise TypeError('Expected str, got something else.')
        if not isinstance(updated_fields_dict, dict):
            raise TypeError('Expected a dict, got something else.')
        return self.museum_repo.update_museum(museum_id, updated_fields_dict)
    
    def remove_museum(self, museum_id: str) -> str:
        if not isinstance(museum_id, str):
            raise TypeError('Expected str, got something else.')
        return self.museum_repo.remove_museum(museum_id)

