from uuid import UUID
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from src.core._shared.views import BaseListViewSet
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
)
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
)
from src.django_project.category_app.serializers import (
    CreateCategoryInputSerializer,
    CreateCategoryOutputSerializer,
    ListCategoriesOutputSerializer,
    RetrieveCategoryInputSerializer,
    RetrieveCategoryOutputSerializer,
    DeleteCategoryInputSerializer,
    ListCategoriesOutputSerializer,
    RetrieveCategoryInputSerializer,
    RetrieveCategoryOutputSerializer,
    UpdateCategoryInputSerializer,
)

class CategoryViewSet(BaseListViewSet):
    list_use_case = ListCategory
    list_serializer_class = ListCategoriesOutputSerializer
    repository = DjangoORMCategoryRepository

    def retrieve(self, request: Request, pk: UUID) -> Response:
        serializer = RetrieveCategoryInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetCategory.Input(id=serializer.validated_data["id"])
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            result = use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryOutputSerializer(instance=result)
        return Response(
            status=HTTP_200_OK,
            data=category_output.data,
        )

    def create(self, request: Request) -> Response:
        """
        Create a new category.
        """
        serializer = CreateCategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategory.Input(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryOutputSerializer(instance=output).data,
        )

    def update(self, request: Request, pk=None) -> Response:
        """
        Update an existing category.
        """
        serializer = UpdateCategoryInputSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCategory.Input(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        """
        Delete an existing category.
        """
        serializer = DeleteCategoryInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

        try:
            use_case.execute(request=DeleteCategory.Input(**serializer.validated_data))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request: Request, pk=None) -> Response:
        """
        Partially update an existing category.
        """
        serializer = UpdateCategoryInputSerializer(
            data={**request.data, "id": pk}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategory.Input(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
