from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    """
    Base model to apply a UUID PK.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
