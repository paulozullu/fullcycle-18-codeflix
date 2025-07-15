from rest_framework import serializers

from src.core._shared.serializer import ListOutputMetaSerializer


class CategoryOutputSerializer(serializers.Serializer):
    """
    Serializer for the Category response.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoriesOutputSerializer(serializers.Serializer):
    """
    Serializer for the List Categories response.
    """

    data = CategoryOutputSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveCategoryOutputSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Category response.
    """

    data = CategoryOutputSerializer(source="*")


class RetrieveCategoryInputSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Category request.
    """

    id = serializers.UUIDField()


class CreateCategoryInputSerializer(serializers.Serializer):
    """
    Serializer for the Create Category request.
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class CreateCategoryOutputSerializer(serializers.Serializer):
    """
    Serializer for the Create Category response.
    """

    id = serializers.UUIDField()


class UpdateCategoryInputSerializer(serializers.Serializer):
    """
    Serializer for the Update Category request.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class DeleteCategoryInputSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Category request.
    """

    id = serializers.UUIDField()
