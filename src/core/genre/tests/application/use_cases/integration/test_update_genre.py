from uuid import uuid4

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def genre_repository():
    return InMemoryGenreRepository()


@pytest.fixture
def category_repository():
    return InMemoryCategoryRepository()


class TestUpdateGenre:
    def test_update_genre_name(self, genre_repository, category_repository):
        category = Category(name="Filmes", description="Filmes em geral")
        category_repository.save(category)

        genre = Genre(name="Terror", categories={category.id})
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )

        request = UpdateGenre.Input(
            id=genre.id,
            name="Action",
            categories={category.id},
        )
        use_case.execute(request)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == "Action"
        assert updated_genre.is_active == True
        assert len(updated_genre.categories) == 1
        assert updated_genre.categories == {category.id}

    def test_activate_genre(self, genre_repository, category_repository):
        category = Category(name="Filmes", description="Filmes em geral")
        category_repository.save(category)

        genre = Genre(name="Terror", categories={category.id}, is_active=False)
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        request = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            categories={category.id},
            is_active=True,
        )
        use_case.execute(request)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == "Terror"
        assert updated_genre.is_active is True
        assert len(updated_genre.categories) == 1
        assert updated_genre.categories == {category.id}

    
        category = Category(name="Filme", description="Filmes em geral")
        repository = InMemoryCategoryRepository()
        repository.save(category)
        id = uuid4()
        request = UpdateCategoryRequest(id=id, name="Teste")
        use_case = UpdateCategory(repository)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

        assert exc.type == CategoryNotFound

    def test_deactivate_genre(self, genre_repository, category_repository):
        category = Category(name="Filmes", description="Filmes em geral")
        category_repository.save(category)

        genre = Genre(name="Terror", categories={category.id})
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        request = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            categories={category.id},
            is_active=False,
        )
        use_case.execute(request)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == "Terror"
        assert updated_genre.is_active is False
        assert len(updated_genre.categories) == 1
        assert updated_genre.categories == {category.id}

    
        category = Category(name="Filme", description="Filmes em geral")
        repository = InMemoryCategoryRepository()
        repository.save(category)
        id = uuid4()
        request = UpdateCategoryRequest(id=id, name="Teste")
        use_case = UpdateCategory(repository)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

        assert exc.type == CategoryNotFound

    def test_add_category(self, genre_repository, category_repository):
        category = Category(name="Filmes", description="Filmes em geral")
        category_repository.save(category)

        genre = Genre(name="Terror", categories={category.id})
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )

        new_category = Category(name="New", description="Lançamentos")
        category_repository.save(new_category)
        request = UpdateGenre.Input(
            id=genre.id,
            name=genre.name,
            categories={category.id, new_category.id},
            is_active=genre.is_active
        )
        use_case.execute(request)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == "Terror"
        assert updated_genre.is_active == genre.is_active
        assert len(updated_genre.categories) == 2
        assert category.id in updated_genre.categories
        assert new_category.id in updated_genre.categories

    def test_remove_cateory(self, genre_repository, category_repository):
        category = Category(name="Filmes", description="Filmes em geral")
        category_repository.save(category)
        other_category = Category(name="New", description="Lançamentos")
        category_repository.save(other_category)

        genre = Genre(name="Terror", categories={category.id, other_category.id})
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )

        request = UpdateGenre.Input(
            id=genre.id,
            name=genre.name,
            categories={category.id},
            is_active=genre.is_active,
        )
        use_case.execute(request)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == genre.name
        assert updated_genre.is_active == genre.is_active
        assert len(updated_genre.categories) == 1
        assert category.id in updated_genre.categories
        assert not other_category.id in updated_genre.categories

    def test_update_genre(self, genre_repository, category_repository):
        category = Category(name="Filmes", description="Filmes em geral")
        category_repository.save(category)

        genre = Genre(name="Terror", categories={category.id})
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )

        new_category = Category(name="New", description="Lançamentos")
        category_repository.save(new_category)
        request = UpdateGenre.Input(
            id=genre.id,
            name="Action",
            categories={category.id, new_category.id},
            is_active=False,
        )
        use_case.execute(request)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == "Action"
        assert updated_genre.is_active == False
        assert len(updated_genre.categories) == 2
        assert category.id in updated_genre.categories
        assert category.id in updated_genre.categories