# Django Imports
from django.db.models.fields.files import ImageFieldFile

# Other Third Party Imports
from inertia.utils import InertiaJsonEncoder


class InertiaCustomJsonEncoder(InertiaJsonEncoder):
    def default(self, value):
        if isinstance(value, ImageFieldFile):
            return value.url if value else ""
        # return super().default(value)
        try:
            return super().default(value)
        except:
            return None
