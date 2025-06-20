from functools import partial
from uuid import UUID, uuid4
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
)

from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import ListGenreOutputSerializer

class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        """
        List all genres.
        """
        input = ListGenre.Input()
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input)
        serializer = ListGenreOutputSerializer(output)
        return Response(status=HTTP_200_OK, data=serializer.data)

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

    # def create(self, request: Request) -> Response:
    #     """
    #     Create a new category.
    #     """
    #     serializer = CreateCategoryRequestSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     input = CreateCategoryRequest(**serializer.validated_data)
    #     use_case = CreateCategory(repository=DjangoORMCategoryRepository())
    #     output = use_case.execute(input)

    #     return Response(
    #         status=HTTP_201_CREATED,
    #         data=CreateCategoryResponseSerializer(instance=output).data,
    #     )

    # def update(self, request: Request, pk=None) -> Response:
    #     """
    #     Update an existing category.
    #     """
    #     serializer = UpdateCategoryRequestSerializer(data={**request.data, "id": pk})
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

    # def destroy(self, request: Request, pk=None) -> Response:
    #     """
    #     Delete an existing category.
    #     """
    #     serializer = DeleteCategoryRequestSerializer(data={"id": pk})
    #     serializer.is_valid(raise_exception=True)

    #     use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

    #     try:
    #         use_case.execute(request=DeleteCategoryRequest(**serializer.validated_data))
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     return Response(status=HTTP_204_NO_CONTENT)
    
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
