from src.domain.museum import Museum

class MockMuseumRepository:
    def get_all_museums(self) -> list[Museum]:
        return [Museum(museum_id = 'test', name = 'test', location = 'test', contact_email = 'test@test.com')]
    
    def add_museum(self, museum: Museum) -> str:
        return 'mock_id'
    
    def get_museum_by_id(self, museum_id: int) -> Museum:
        museum = Museum(
            museum_id = 'test', 
            name = 'test', 
            location = 'test', 
            contact_email = 'test@test.com'
            )
        return museum
    
    def remove_museum(self, museum_id: str) -> str:
        return 'mock_id'
    
    def update_museum(self, museum_id: str, updated_fields_dict: dict) -> str:
        return 'mock_id'