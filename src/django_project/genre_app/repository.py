from src.core.genre.domain.genre import Genre

from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from django.db import transaction


class DjangoORMGenreRepository(GenreRepository):
    def __init__(self, model: GenreModel = GenreModel):
        self.model = model

    def save(self, genre: Genre):
        with transaction.atomic():
            genre_model = self.model.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )

            if genre.categories:
                genre_model.categories.set(genre.categories)

    def get_by_id(self, id: str) -> Genre | None:
        raise NotImplementedError("This method is not implemented yet.")

    def delete(self, id: str):
        raise NotImplementedError("This method is not implemented yet.")

    def find_all(self) -> list[Genre]:
        raise NotImplementedError("This method is not implemented yet.")

    def update(self, genre: Genre):
        raise NotImplementedError("This method is not implemented yet.")
