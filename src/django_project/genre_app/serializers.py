from rest_framework import serializers


class GenreOutputSerializer(serializers.Serializer):
    """
    Serializer for the Genre response.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreOutputSerializer(serializers.Serializer):
    """
    Serializer for the List Genres response.
    """

    data = GenreOutputSerializer(many=True)


class SetField(serializers.ListField):
    """
    Custom field to handle sets in serializers.
    """

    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateGenreInputSerializer(serializers.Serializer):
    """
    Serializer for the Create Genre input.
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(
        child=serializers.UUIDField(),
        help_text="List of category IDs associated with the genre.",
    )


class CreateGenreOutputSerializer(serializers.Serializer):
    """
    Serializer for the Create Genre response.
    """

    id = serializers.UUIDField()


class DeleteGenreInputSerializer(serializers.Serializer):
    """
    Serializer for Delete Genre input.
    """

    id = serializers.UUIDField()


class UpdateGenreInputSerializer(serializers.Serializer):
    """
    Serializer for the Update Genre input.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories = SetField(
        child=serializers.UUIDField(),
        help_text="List of category IDs associated with the genre.",
    )


class RetrieveGenreOutputSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Genre output.
    """

    data = GenreOutputSerializer(source="*")


class RetrieveGenreInputSerializer(serializers.Serializer):
    """
    Serializer for the Retrieve Genre input.
    """

    id = serializers.UUIDField()
