from abc import ABC
from rest_framework import serializers


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class BaseEntityOutputSerializer(serializers.Serializer): ...


class BaseListOutputSerializer(serializers.Serializer):
    """
    Serializer for the List Etities response.
    """
    data = BaseEntityOutputSerializer(many=True)
    meta = ListOutputMetaSerializer()
