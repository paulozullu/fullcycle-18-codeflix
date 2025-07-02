import uuid
from django.db import models
from src.core.cast_member.domain.cast_member import Type


class CastMember(models.Model):
    app_label = "cast_member_app"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=30,
        choices=[(t.value, t.value) for t in Type],
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"CastMember(id={self.id}, name={self.name}, type={self.type})"

    class Meta:
        db_table = "cast_member"
