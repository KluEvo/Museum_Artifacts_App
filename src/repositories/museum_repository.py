from sqlalchemy.orm import Session
from src.domain.museum import Museum
from src.repositories.museum_repository_protocol import MuseumRepositoryProtocol

class MuseumRepository(MuseumRepositoryProtocol):
    def __init__(self, session: Session):
        self.session = session

    def get_all_museums(self) -> list[Museum]:
        return self.session.query(Museum).all()
    
    def add_museum(self, museum: Museum) -> Museum:
        self.session.add(museum)
        self.session.commit()
        self.session.refresh(museum)
        return str(museum.museum_id)
    
    def get_museum_by_id(self, museum_id: int) -> Museum:
        museum = self.session.query(Museum).filter(Museum.museum_id == museum_id).first()
        if not museum:
            raise ValueError(f"Museum not found: {museum_id}")
        return museum
    
    def remove_museum(self, museum_id: str) -> str:
        museum = self.session.query(Museum).filter(Museum.museum_id == museum_id).first()
        if not museum:
            raise ValueError(f"Museum not found: {museum_id}")
        self.session.delete(museum)
        self.session.commit()
        return str(museum.museum_id)
    
    def update_museum(self, museum_id: str, updated_fields_dict: dict) -> str:
        museum = self.session.get(Museum, museum_id)
        if museum is None:
            raise ValueError(f"Museum not found: {museum_id}")

        allowed_fields = {col.name for col in Museum.__table__.columns if not col.primary_key}

        for field, value in updated_fields_dict.items():
            if field not in allowed_fields:
                raise ValueError(f"Field not updatable: {field}")
            setattr(museum, field, value)

        self.session.commit()
        self.session.refresh(museum)
        return str(museum.museum_id)
