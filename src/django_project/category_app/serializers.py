from rest_framework import serializers

from src.core._shared.serializer import ListOutputMetaSerializer


class CategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for the Category response.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoriesResponseSerializer(serializers.Serializer):
    """
    Serializer for the List Categories response.
    """

    data = CategoryResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Category response.
    """

    data = CategoryResponseSerializer(source="*")


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Category request.
    """

    id = serializers.UUIDField()


class CreateCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for the Create Category request.
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class CreateCategoryResponseSerializer(serializers.Serializer):
    """
    Serializer for the Create Category response.
    """

    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for the Update Category request.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class DeleteCategoryRequestSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Category request.
    """

    id = serializers.UUIDField()
