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


# class RetrieveGenreResponseSerializer(serializers.Serializer):
#     """
#     Serializer for the Retrieve Genre response.
#     """

#     data = GenreResponseSerializer(source="*")


# class RetrieveGenreRequestSerializer(serializers.Serializer):
#     """
#     Serializer for the Retrieve Genre request.
#     """

#     id = serializers.UUIDField()


# class CreateGenreRequestSerializer(serializers.Serializer):
#     """
#     Serializer for the Create Genre request.
#     """

#     name = serializers.CharField(max_length=255, allow_blank=False)
#     description = serializers.CharField()
#     is_active = serializers.BooleanField(default=True)


# class CreateGenreResponseSerializer(serializers.Serializer):
#     """
#     Serializer for the Create Genre response.
#     """

#     id = serializers.UUIDField()


# class UpdateGenreRequestSerializer(serializers.Serializer):
#     """
#     Serializer for the Update Genre request.
#     """

#     id = serializers.UUIDField()
#     name = serializers.CharField(max_length=255, allow_blank=False)
#     description = serializers.CharField()
#     is_active = serializers.BooleanField()


# class DeleteGenreRequestSerializer(serializers.Serializer):
#     """
#     Serializer for the Retrieve Genre request.
#     """

#     id = serializers.UUIDField()
