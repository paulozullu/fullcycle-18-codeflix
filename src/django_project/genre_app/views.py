from functools import partial
from http import HTTPStatus
from uuid import UUID, uuid4
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
)

from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreOutputSerializer,
    DeleteGenreInputSerializer,
    ListGenreOutputSerializer,
    UpdateGenreInputSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        """
        List all genres.
        """
        input = ListGenre.Input()
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input)
        serializer = ListGenreOutputSerializer(output)
        return Response(status=HTTPStatus.OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        """
        Create a new genre.
        """
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )

        try:
            output = use_case.execute(input)
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(
                status=HTTPStatus.BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreOutputSerializer(instance=output).data,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        """
        Delete an existing genre.
        """
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteGenre(repository=DjangoORMGenreRepository())

        try:
            use_case.execute(input=DeleteGenre.Input(**serializer.validated_data))
        except GenreNotFound:
            return Response(status=HTTPStatus.NOT_FOUND)

        return Response(status=HTTPStatus.NO_CONTENT)

    def update(self, request: Request, pk=None) -> Response:
        """
        Update an existing genre.
        """
        serializer = UpdateGenreInputSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )

        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTPStatus.NOT_FOUND)
        except RelatedCategoriesNotFound:
            return Response(status=HTTPStatus.BAD_REQUEST)

        return Response(status=HTTPStatus.NO_CONTENT)

    # def retrieve(self, request: Request, pk: UUID) -> Response:
    #     serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
    #     serializer.is_valid(raise_exception=True)

    #     request = GetCategoryRequest(id=serializer.validated_data["id"])
    #     use_case = GetCategory(repository=DjangoORMCategoryRepository())

    #     try:
    #         result = use_case.execute(request=request)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     category_output = RetrieveCategoryResponseSerializer(instance=result)
    #     return Response(
    #         status=HTTP_200_OK,
    #         data=category_output.data,
    #     )

    # def partial_update(self, request: Request, pk=None) -> Response:
    #     """
    #     Partially update an existing category.
    #     """
    #     serializer = UpdateCategoryRequestSerializer(data={**request.data, "id": pk}, partial=True)
    #     serializer.is_valid(raise_exception=True)

    #     input = UpdateCategoryRequest(**serializer.validated_data)
    #     use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

    #     try:
    #         use_case.execute(request=input)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     return Response(
    #         status=HTTP_204_NO_CONTENT,
    #     )
