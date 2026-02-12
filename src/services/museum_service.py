from src.repositories.museum_repository_protocol import MuseumRepositoryProtocol
from src.domain.museum import Museum
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)


class MuseumService:
    def __init__(self, museum_repo: MuseumRepositoryProtocol):
        self.museum_repo = museum_repo

    def add_museum(self, museum: Museum) -> str:
        if not isinstance(museum, Museum):
            raise ValidationException("Invalid museum object provided.")

        try:
            return self.museum_repo.add_museum(museum)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error while adding museum."
            ) from e
    
    def get_museum_by_id(self, museum_id: str) -> Museum:
        if not isinstance(museum_id, str):
            raise ValidationException("Museum ID must be a string.")

        try:
            return self.museum_repo.get_museum_by_id(museum_id)
        except ValueError:
            raise NotFoundException(
                f"Museum with id {museum_id} not found."
            )
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error while retrieving museum."
            ) from e


    def get_all_museums(self) -> str:
        try:
            return self.museum_repo.get_all_museums()
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error while retrieving museums."
            ) from e

    def update_museum(self, museum_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(museum_id, str):
            raise ValidationException("Museum ID must be a string.")
        if not isinstance(updated_fields_dict, dict):
            raise ValidationException(
                "Updated fields must be a dictionary."
            )

        try:
            return self.museum_repo.update_museum(museum_id, updated_fields_dict)
        except ValueError as e:
            raise NotFoundException(str(e))
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error while updating museum."
            ) from e
    
    def remove_museum(self, museum_id: str) -> str:
        if not isinstance(museum_id, str):
            raise ValidationException("Museum ID must be a string.")

        try:
            return self.museum_repo.remove_museum(museum_id)
        except ValueError:
            raise NotFoundException(
                f"Museum with id {museum_id} not found."
            )
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error while removing museum."
            ) from e
