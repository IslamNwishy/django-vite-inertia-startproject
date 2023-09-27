# Python Standard Library Imports
import json
import re

# Django Imports
from django.core.exceptions import ImproperlyConfigured
from django.http import QueryDict

# Other Third Party Imports
from inertia import lazy, render

from utils.inertia_utils.inertia_form_mixin import InertiaFormMixin


class InertiaTemplateMixin:
    template_name = None
    title = ""

    def get_title(self):
        """return a title for the rendered page"""
        return self.title

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault("content_type", self.content_type)
        context.pop("site", None)
        context["view"] = self.get_title()

        context = self.serialize_list_response(context)

        return render(
            self.request,
            self.get_template_name(),
            context,
        )

    def serialize_list_response(self, context):
        """
        serialize the typical response from ListView.
        change it if you want the ListView to return a different response schema
        """

        paginator = context.pop("paginator", None)
        if paginator:
            context["page_obj"] = {
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "per_page": paginator.per_page,
                "number": context["page_obj"].number,
            }

        # will use form_class for field serialization
        # if it does not exist object list will return normally as a queryset
        object_list = context.get("object_list")
        if object_list and hasattr(self, "form_class"):
            form = self.get_form_class()
            context["object_list"] = [
                {"fields": form(instance=obj).serialize_fields(True), "id": obj.id}
                for obj in object_list
            ]
            context["page_obj"]["headers"] = [
                {"name": field["name"], "label": field["label"]}
                for field in context["object_list"][0]["fields"]
            ]

        return context

    def get_template_name(self):
        """
        Return template name to be used for the request.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "InertiaTemplateMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'"
            )
        else:
            return self.template_name

    def get_context_object_name(self, object_list):
        return None

    def get_form_class(self):
        return getattr(self, "form_class", None)


class InertiaViewMixin(InertiaTemplateMixin):
    permission_checks = []

    def dispatch(self, *args, **kwargs):
        func = super().dispatch
        for check in self.permission_checks:
            func = check(func)

        return func(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Serialize a form for inertia if found"""
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        if form:
            if not isinstance(form, InertiaFormMixin):
                raise ImproperlyConfigured(
                    f"{type(form).__name__} must inherit from inertia_utils.inertia_form_mixin.InertiaFormMixin"
                )
            context["form"], context["errors"] = form.serialize_form()

        return context

    def get_form_class(self):
        old_form = super().get_form_class()
        if not issubclass(old_form, InertiaFormMixin):
            return type(
                f"Inertia{type(old_form).__name__}", (InertiaFormMixin, old_form), {}
            )

        return old_form
