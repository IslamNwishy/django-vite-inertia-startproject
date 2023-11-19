# Python Standard Library Imports
import logging
import re
from copy import copy
from types import MethodType

# Django Imports
from django.core.exceptions import ImproperlyConfigured
from django.forms import HiddenInput
from django.http import HttpResponse
from django.urls import resolve

# Other Third Party Imports
from inertia import lazy, render
from utils.inertia_utils.inertia_form_mixin import InertiaFormMixin


def custom_build_uri(self, location=None):
    referer = self.headers.get("X-Inertia-Referer")
    url = None
    if (
        referer
        and getattr(self, "preserve_url", False)
        or self.GET.get("preserve_url") in [True, "true"]
        or self.POST.get("preserve_url") in [True, "true"]
    ):
        url = referer

    return type(self).build_absolute_uri(self, url or location)


class InertiaTemplateMixin:
    template_name = None
    title = ""
    minimal = False
    parent_view = None
    is_modal = False
    can_hold_modal = True
    template_extras = {}

    def dispatch(self, *args, **kwargs):
        if not getattr(self.request, "faked", False):
            self.template_extras = self.generate_template_name()
        return super().dispatch(*args, **kwargs)

    @classmethod
    def get_view_name(cls):
        return cls.__name__.removesuffix("View")

    def get_title(self):
        """return a title for the rendered page"""
        return self.title or re.sub(r"(\w)([A-Z])", r"\1 \2", self.get_view_name())

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        if getattr(self.request, "faked", False):
            return HttpResponse()

        context.pop("site", None)
        context["view"] = self.get_view_name()
        if self.parent_view:
            context["subview"] = context["view"]
            context["view"] = self.parent_view.get_view_name()

        context["title"] = self.get_title()
        context["success_url"] = self.get_success_url()
        context["current_url"] = self.request.get_full_path()
        context["__EXTRAS__"] = self.template_extras
        self.request.build_absolute_uri = MethodType(custom_build_uri, self.request)
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

        # will use form_class for field serialization
        # if it does not exist object list will return normally as a queryset
        object_list = context.get("object_list")
        if object_list and hasattr(self, "form_class"):
            form = self.get_form_class()
            context["object_list"] = lambda: [
                {
                    "fields": form(instance=obj).serialize_fields(read_only=True, minimal=self.minimal),
                    "id": obj.id,
                }
                for obj in object_list
            ]

        one_obj = context.get("object")
        if one_obj and hasattr(self, "form_class"):
            form = self.get_form_class()
            context["object"] = lambda: {
                **form(instance=one_obj).serialize_fields(read_only=True, minimal=True),
                "id": one_obj.id,
            }

        paginator = context.pop("paginator", None)
        if paginator:
            page_num = context["page_obj"].number
            context["page_obj"] = lambda: {
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "per_page": paginator.per_page,
                "number": page_num,
                "headers": [
                    {"name": field["name"], "label": field["label"]} for field in context["object_list"]()[0]["fields"]
                ]
                if not self.minimal
                else [],
            }

        filterset = context.pop("filter", None)
        if filterset:
            context["filter_form"] = self.serialize_filterset(filterset)
        return context

    def serialize_filterset(self, filterset):
        return lambda: type(
            f"Inertia{type(filterset.form.__class__).__name__}",
            (InertiaFormMixin, filterset.form.__class__),
            {},
        )(filterset.form.data).serialize_form()

    def generate_template_name(self):
        if self.is_modal:
            referer = self.request.headers.get("X-Inertia-Referer")
            if referer:
                base_path = referer.split("?", 1)[0]
                try:
                    view_cls = resolve(base_path).func.view_class
                    if view_cls.is_modal:
                        base_path = self.request.session.get("last_page")
                        view_cls = resolve(base_path).func.view_class if base_path else None
                except Exception as e:
                    logging.warning(
                        f"ERROR {e} while trying to get the base page for the modal {self.__class__.__name__}"
                    )
                    view_cls = None

                if view_cls and view_cls.can_hold_modal:
                    self.parent_view = view_cls
                    self.request.session["last_page"] = base_path
                    self.last_page_url = base_path
                    return {"base": view_cls.template_name, "modal": self.template_name, "stale": True}

            if not self.parent_view:
                raise ImproperlyConfigured("Modal views must have a parent view")

            self.last_page_url = self.get_success_url()
            self.request.session["last_page"] = None
            return {"base": self.parent_view.template_name, "modal": self.template_name}

        self.request.session["last_page"] = None
        return {"base": self.template_name}

    def get_template_name(self):
        """
        Return template name to be used for the request.
        """
        if not isinstance(self.template_name, str):
            raise ImproperlyConfigured(
                "InertiaTemplateMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'"
            )

        return self.template_extras["base"]

    def get_context_object_name(self, object_list):
        return None

    def get_form_class(self):
        if hasattr(super(), "get_form_class"):
            return super().get_form_class()
        return getattr(self, "form_class", None)


class InertiaViewMixin(InertiaTemplateMixin):
    permission_checks = []
    submit_button_text = None
    allow_hide = False

    def dispatch(self, *args, **kwargs):
        func = super().dispatch
        for check in self.permission_checks:
            func = check(func)

        return func(*args, **kwargs)

    def serialize_form(self, form):
        """Serialize a form for inertia"""
        if not isinstance(form, InertiaFormMixin):
            raise ImproperlyConfigured(
                f"{type(form).__name__} must inherit from inertia_utils.inertia_form_mixin.InertiaFormMixin"
            )

        return lambda: form.serialize_form(self.submit_button_text), form.serialize_errors

    def paginate_form_field(self):
        field_name, offset, limit, query = (
            self.request.GET.get("field"),
            self.request.GET.get("offset"),
            self.request.GET.get("limit"),
            self.request.GET.get("query"),
        )
        form = self.get_form()
        if not (field_name or offset):
            logging.warning(f"paginate field must have a field and offset but got {self.request.GET}")
            return {}

        setattr(self.request, "preserve_url", True)
        choices, offset, limit = form.paginate_field(field_name, int(offset), int(limit) if limit else None, query)
        return {
            "newChoices": choices,
            "newOffset": offset,
            "newLimit": limit,
            "query": query,
        }

    def get_context_data(self, **kwargs):
        """Serialize a form for inertia if found"""
        context = super().get_context_data(**kwargs)
        if not getattr(self.request, "faked", False):
            context["paginate"] = lazy(self.paginate_form_field)

        form = context.get("form")
        if form:
            if isinstance(form, list):
                form_array, errors_array = [], []
                for f in form:
                    form, errors = self.serialize_form(f)
                    form_array.append(form)
                    errors_array.append(errors)
                context["form"] = form_array
                context["errors"] = errors_array

            else:
                context["form"], context["errors"] = self.serialize_form(form)

        context = self.serialize_list_response(context)

        if self.parent_view:
            fake_request = copy(self.request)
            fake_request.method = "GET"
            setattr(fake_request, "faked", True)
            parent_view = self.parent_view()
            try:
                parent_view.setup(request=fake_request)
                parent_view.dispatch(fake_request)
                parent_context = parent_view.get_context_data()
            except:
                parent_context = {}
            if self.template_extras.get("stale", False):
                refresh_context_attrs = []
                for key, value in parent_context.items():
                    if callable(value):
                        parent_context[key] = lazy(value)
                        refresh_context_attrs.append(key)
                parent_context["refresh_context_attrs"] = refresh_context_attrs

            if self.is_modal and self.last_page_url is None:
                logging.warning(
                    f"last_page_url is sent as None for modal {self.__class__.__name__} which can cause issues with the modal behaviour on exit. make sure you have a success_url setup on the view"
                )

            parent_context["last_page_url"] = self.last_page_url
            parent_context.update(context)
            return parent_context

        return context

    def get_form_class(self):
        old_form = super().get_form_class()
        if not issubclass(old_form, InertiaFormMixin):
            return type(f"Inertia{old_form.__name__}", (InertiaFormMixin, old_form), {})

        return old_form

    def get_success_url(self, *args, **kwargs):
        # should stay in the same page
        if self.request.POST.get("stay") in [True, "true"] or self.request.GET.get("stay") in [True, "true"]:
            return self.request.path_info

        # given a next path
        next_path = self.request.GET.get("next") or self.request.POST.get("next")
        if next_path:
            return next_path

        # given a success url
        success_url = getattr(self, "success_url", None)
        try:
            return super().get_success_url(*args, **kwargs)
        except:
            return success_url

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        hide = self.request.GET.get("hide")
        if self.allow_hide and hide:
            for field_name in hide.split(","):
                form.fields[field_name].widget = HiddenInput()

        return form
