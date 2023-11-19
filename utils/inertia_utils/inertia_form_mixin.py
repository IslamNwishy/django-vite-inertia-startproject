# Python Standard Library Imports
import json

# Django Imports
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

FORM_META = ["data", "files", "is_bound", "empty_permitted"]
FORM_FIELD_ATTRS = ["strip", "show_hidden_initial", "help_text", "initial"]
RENAME_FIELDS = {
    "minlength": {"text": "minLength", "default": "min"},
    "maxlength": {"text": "maxLength", "default": "max"},
    "autofocus": {"default": "autoFocus"},
    "autocapitalize": {"default": "autoCapitalize"},
    "autocomplete": {"default": "autoComplete"},
}
TYPE_MAPPING = {
    forms.DateInput: "date",
    forms.DateTimeInput: "datetime-local",
    forms.TimeInput: "time",
    forms.Textarea: "textarea",
}
READONLY_DEFAULT_POSTPROCESS = {
    forms.ModelMultipleChoiceField: lambda data: ", ".join([str(obj) for obj in data]),
    forms.ModelChoiceField: str,
}


class InertiaFormMixin:
    submit_button_text = "Submit"
    DEFAULT_PAGE_SIZE = 10

    def get_submit_button_text(self):
        """return the text to show for the submit button"""
        return self.submit_button_text

    def serialize_form(self, submit_button_text=None):
        """Serialize a django form into dict"""
        form_data = {attr: getattr(self, attr, None) for attr in FORM_META}
        form_data["fields"] = self.serialize_fields()
        form_data["initial"] = {
            field["name"]: self.get_inertia_initial(field["value"], field["attrs"].get("multiple"))
            for field in form_data["fields"]
        }
        form_data["data"] = dict(form_data["data"])
        form_data["submit_button_text"] = submit_button_text or self.get_submit_button_text()
        return form_data

    def serialize_errors(self):
        return json.loads(self.errors.as_json())

    def serialize_fields(self, read_only=False, minimal=False, include=[], exclude=[], include_id=False):
        """serialize django form field into dict"""
        field_whitelist = include or self.fields.keys()
        field_whitelist = set(field_whitelist) - set(exclude)
        if minimal:
            serialized_fields = {
                name: self.get_inertia_field(field, name, read_only, minimal)
                for name, field in self.fields.items()
                if name in field_whitelist
            }
            if include_id:
                serialized_fields["id"] = self.instance.id

            return serialized_fields

        return [
            self.get_inertia_field(field, name, read_only)
            for name, field in self.fields.items()
            if name in field_whitelist
        ]

    def get_inertia_field(self, field, name, read_only, minimal=False):
        """serialize a form field"""

        widget = field.widget
        field = forms.BoundField(self, field, name)
        if minimal:
            return {
                "label": str(field.label),
                "value": self._get_readonly_value(field.field, field.value(), name) if read_only else field.value(),
            }
        widget_attrs = widget.attrs.copy()
        field_data = {attr: getattr(field, attr, None) for attr in FORM_FIELD_ATTRS}

        # these will passed to the actual html field
        field_type = TYPE_MAPPING.get(type(widget), getattr(widget, "input_type", "text"))
        meta_attrs = {"type": field_type, "required": field.field.required, "disabled": field.field.disabled}
        multiple = getattr(widget, "allow_multiple_selected", None)
        if multiple:
            meta_attrs["multiple"] = True
        for key, value in widget_attrs.items():
            if key in RENAME_FIELDS:
                key = RENAME_FIELDS[key].get(field_type, RENAME_FIELDS[key].get("default", key))
            meta_attrs[key] = value

        field_data["attrs"] = meta_attrs

        # used to define the behaviour of the field but should not be passed directly to html
        field_data["name"] = name
        field_data["id"] = field.html_initial_id
        field_data["label"] = str(field.label)
        field_data["value"] = field.value()
        if getattr(self, "instance", None):
            if read_only:
                field_data["value"] = self._get_readonly_value(field.field, field_data["value"], name)
            elif meta_attrs.get("disabled"):
                field_data["readonly_data"] = self._get_readonly_value(field.field, field_data["value"], name)

        choices = getattr(widget, "choices", None)
        if choices and not (meta_attrs.get("type") == "hidden" or meta_attrs.get("disabled")):
            if isinstance(field.field, forms.ModelChoiceField):
                field_choices, field_data["offset"], field_data["limit"] = self.paginate_field(name)
            else:
                field_choices = [[str(choice[0]), choice[1]] for choice in choices]

            field_data["choices"] = field_choices

        return field_data

    def paginate_field(self, field_name, offset=0, limit=None, query=None):
        if limit is None:
            limit = self.DEFAULT_PAGE_SIZE

        field = self.fields.get(field_name)
        if isinstance(field, forms.ModelChoiceField):
            value = forms.BoundField(self, field, field_name).value()
            new_offset = offset + limit
            choices = []
            queryset = field.queryset
            model = queryset.model
            search_fields = model.get_search_fields()
            if not search_fields:
                if hasattr(model, "name"):
                    search_fields = ["name__icontains"]
                else:
                    raise ImproperlyConfigured(f"Model {model.__name__} does not have any search fields")

            if query:
                search_query = Q(**{search_fields[0]: query})
                for search_key in search_fields[1:]:
                    search_query |= Q(**{search_key: query})
                queryset = queryset.filter(search_query)
            elif value:
                chosen = field.to_python(value)
                if offset == 0:
                    choices.append([str(chosen.pk), str(chosen)])

                queryset = queryset.exclude(pk=chosen.pk)

            if not queryset.ordered:
                queryset = queryset.order_by(*(model._meta.ordering or ["pk"]))

            for choice in queryset[offset:new_offset]:
                choices.append([str(choice.pk), str(choice)])

            return choices, new_offset, limit

        return [], offset, limit

    def _get_readonly_value(self, field, value, name):
        """
        serialize the field value for viewing (similar to DRF's SerializerMethodField)

        Usage:
            in the form add a function in the format readonly_<field_name>

        Example:

        class ExampleForm(InertiaForm):
            ...
            info = forms.CharField()
            ...

            def readonly_info(self, value):
                return value.replace('\n', ',')

        """
        obj = field.to_python(value)
        func = getattr(self, f"readonly_{name}", READONLY_DEFAULT_POSTPROCESS.get(type(field)))
        if func:
            return func(obj)

        return value

    @staticmethod
    def get_inertia_initial(initial, multiple=False):
        """get the initial data of a field"""
        if initial is None:
            if multiple:
                return []
            return ""
        return initial


class InertiaModelForm(InertiaFormMixin, forms.ModelForm):
    """ModelForm that supports being passed to inertia"""


class InertiaForm(InertiaFormMixin, forms.Form):
    """Form that supports being passed to inertia"""
