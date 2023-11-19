# Django Imports
from django.db import models


class AbstractModelFunctionsMixin:
    search_fields = []

    @classmethod
    def get_all_field_names(cls, exclude=[], include_reverse=[], *args, **kwargs):
        """
        returns all field names of this model
        exclude: a list of fields that will be ignored if found
        """
        if not kwargs.get("include_parents", True):
            exclude += ["id", "is_active", "created_at", "updated_at"]

        if include_reverse is not True:
            for field in cls._meta.related_objects:
                related_field_name = field.related_name or field.related_model.__name__.lower()
                if related_field_name not in include_reverse:
                    exclude.append(related_field_name)

        fields = [field.name for field in cls._meta.get_fields(*args, **kwargs) if field.name not in exclude]
        return fields

    @classmethod
    def get_search_fields(cls):
        return cls.search_fields


class AbstractModel(models.Model, AbstractModelFunctionsMixin):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
