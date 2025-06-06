import uuid
from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active})"

    class Meta:
        db_table = "category"
