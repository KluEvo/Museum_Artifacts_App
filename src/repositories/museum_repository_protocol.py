from typing import List, Protocol
from src.domain.museum import Museum

class MuseumRepositoryProtocol(Protocol):
    def get_all_museums(self) -> List[Museum]:
        ...

    def add_museum(self, museum:Museum) -> str:
        ...

    def get_museum_by_id(self, museum_id:str) -> Museum:
        ...
        
    def remove_museum(self, museum_id:str) -> str:
        ...

    def update_museum(self, museum_id:str, updated_fields_dict: dict) -> str:
        ...
