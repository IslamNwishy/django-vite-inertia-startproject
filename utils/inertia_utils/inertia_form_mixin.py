# Python Standard Library Imports
import json

# Django Imports
from django import forms
from django.db.models import Model

# Other Third Party Imports
from utils.json_utils import is_jsonable

FORM_META = ["cleaned_data", "data", "files", "is_bound", "empty_permitted"]
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

    def get_submit_button_text(self):
        """return the text to show for the submit button"""
        return self.submit_button_text

    def serialize_form(self):
        """Serialize a django form into dict"""
        form_data = {attr: getattr(self, attr, None) for attr in FORM_META}
        form_data["fields"] = self.serialize_fields()
        form_data["initial"] = {
            field["name"]: self.get_inertia_initial(
                field["value"], field["attrs"].get("multiple")
            )
            for field in form_data["fields"]
        }
        form_data["data"] = dict(form_data["data"])
        form_data["submit_button_text"] = self.get_submit_button_text()
        return form_data, json.loads(self.errors.as_json())

    def serialize_fields(self, read_only=False):
        """serialize django form field into dict"""

        return [
            self.get_inertia_field(field, name, read_only)
            for name, field in self.fields.items()
        ]

    def get_inertia_field(self, field, name, read_only):
        """serialize a form field"""
        widget = field.widget
        field = forms.BoundField(self, field, name)

        widget_attrs = field.build_widget_attrs({}, widget)
        field_data = {attr: getattr(field, attr, None) for attr in FORM_FIELD_ATTRS}

        # these will passed to the actual html field
        field_type = TYPE_MAPPING.get(
            type(widget), getattr(widget, "input_type", "text")
        )
        meta_attrs = {"type": field_type}
        multiple = getattr(widget, "allow_multiple_selected", None)
        if multiple:
            meta_attrs["multiple"] = True
        for key, value in widget_attrs.items():
            if key in RENAME_FIELDS:
                key = RENAME_FIELDS[key].get(
                    field_type, RENAME_FIELDS[key].get("default", key)
                )
            meta_attrs[key] = value

        field_data["attrs"] = meta_attrs

        # used to define the behaviour of the field but should not be passed directly to html
        field_data["name"] = name
        field_data["id"] = field.html_initial_id
        field_data["label"] = str(field.label)
        field_data["value"] = field.value()
        if read_only and self.instance:
            field_data["value"] = self._get_readonly_value(
                field.field, field_data["value"], name
            )

        choices = getattr(widget, "choices", None)
        if choices:
            field_data["choices"] = [[str(choice[0]), choice[1]] for choice in choices]

        return field_data

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
        func = getattr(
            self, f"readonly_{name}", READONLY_DEFAULT_POSTPROCESS.get(type(field))
        )
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
