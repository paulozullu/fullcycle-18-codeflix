from src.core.genre.domain.genre import Genre
from typing import Optional

from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.category_app.models import Category as CategoryModel
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
            genre_model.save()
            if genre.categories:
                # Buscar instâncias de Category a partir dos IDs
                categories = CategoryModel.objects.filter(id__in=genre.categories)
                genre_model.categories.set(categories)
                genre_model.save()
            return genre

    def get_by_id(self, id: str) -> Optional[Genre]:
        try:
            genre_model = self.model.objects.get(id=id)
            return Genre(
                name=genre_model.name,
                id=genre_model.id,
                is_active=genre_model.is_active,
                categories={category.id for category in genre_model.categories.all()},
            )
        except self.model.DoesNotExist:
            return None

    def delete(self, id: str):
        self.model.objects.filter(id=id).delete()

    def find_all(self) -> list[Genre]:
        for genre_model in self.model.objects.all():
            genre_model
        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories={category.id for category in genre_model.categories.all()},
            )
            for genre_model in self.model.objects.all()
        ]

    def update(self, genre: Genre):
        try:
            genre_model = self.model.objects.get(id=genre.id)
        except self.model.DoesNotExist:
            return None

        with transaction.atomic():
            self.model.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)
