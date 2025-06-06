import uuid
from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        'category_app.Category',
        related_name='genres',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Genre(id={self.id}, name={self.name}, is_active={self.is_active})"

    class Meta:
        db_table = "genre"
