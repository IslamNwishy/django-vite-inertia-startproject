# Django Imports
from django.contrib import admin

# Other Third Party Imports
from utils.abstract_model import AbstractModel


class AbstractModelAdmin(admin.ModelAdmin):
    """an abstract model to automate repetative admin setup"""

    include_reverse = []
    show_first_count = 5
    list_display = []

    def __init__(self, model, admin_site):
        if issubclass(model, AbstractModel):
            if not self.list_display:
                self.list_display = model.get_all_field_names(
                    exclude=["updated_at", "created_at", "is_active"],
                    include_reverse=self.include_reverse,
                    include_parents=False,
                )[: self.show_first_count]
                self.list_display += ["created_at", "is_active"]
        else:
            self.list_display = ("__str__",)

        super().__init__(model, admin_site)
