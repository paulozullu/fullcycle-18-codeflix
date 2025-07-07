from rest_framework import serializers

from src.core.cast_member.domain.cast_member import Type


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        # Utilizamos o "choices" do DRF, que permite um conjunto de opções limitado para um certo campo.
        choices = [(type.value) for type in Type]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Valor vindo da API como "str" é convertido para o StrEnum
        return Type(super().to_internal_value(data))

    def to_representation(self, value):
        # O valor vindo do nosso domínio é convertido para uma string na API
        return str(super().to_representation(value))


class CastMemberOutputSerializer(serializers.Serializer):
    """
    Serializer for the CastMember response.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class ListCastMemberOutputSerializer(serializers.Serializer):
    """
    Serializer for the List CastMembers response.
    """

    data = CastMemberOutputSerializer(many=True)


class CreateCastMemberInputSerializer(serializers.Serializer):
    """
    Serializer for the Create CastMember input.
    """

    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()


class CreateCastMemberOutputSerializer(serializers.Serializer):
    """
    Serializer for the Create CastMember response.
    """

    id = serializers.UUIDField()


class DeleteCastMemberInputSerializer(serializers.Serializer):
    """
    Serializer for Delete CastMember input.
    """

    id = serializers.UUIDField()


class UpdateCastMemberInputSerializer(serializers.Serializer):
    """
    Serializer for the Update CastMember input.
    """

    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()
