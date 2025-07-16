from http import HTTPStatus
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
)

from src.core._shared.views import BaseViewSet
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberInputSerializer,
    CreateCastMemberOutputSerializer,
    DeleteCastMemberInputSerializer,
    ListCastMemberOutputSerializer,
    UpdateCastMemberInputSerializer,
)


class CastMemberViewSet(BaseViewSet):
    list_use_case = ListCastMember
    list_serializer_class = ListCastMemberOutputSerializer
    repository = DjangoORMCastMemberRepository

    def create(self, request: Request) -> Response:
        """
        Create a new cast member.
        """
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCastMember.Input(**serializer.validated_data)
        use_case = CreateCastMember(
            repository=DjangoORMCastMemberRepository(),
        )

        try:
            output = use_case.execute(input)
        except InvalidCastMember as e:
            return Response(
                status=HTTPStatus.BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberOutputSerializer(instance=output).data,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        """
        Delete an existing cast member.
        """
        serializer = DeleteCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())

        try:
            use_case.execute(input=DeleteCastMember.Input(**serializer.validated_data))
        except CastMemberNotFound:
            return Response(status=HTTPStatus.NOT_FOUND)

        return Response(status=HTTPStatus.NO_CONTENT)

    def update(self, request: Request, pk=None) -> Response:
        """
        Update an existing cast member.
        """
        serializer = UpdateCastMemberInputSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCastMember.Input(**serializer.validated_data)
        use_case = UpdateCastMember(
            repository=DjangoORMCastMemberRepository(),
        )

        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(status=HTTPStatus.NOT_FOUND)
        except InvalidCastMember as e:
            return Response(
                status=HTTPStatus.BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(status=HTTPStatus.NO_CONTENT)
