# Django Imports
from django.db.models import Q


class SearchMixin:
    search_fields = []

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query and self.search_fields:
            search_query = Q(**{self.search_fields[0]: query})
            for search_key in self.search_fields[1:]:
                search_query |= Q(**{search_key: query})

            qs = qs.filter(search_query)
        return qs

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, search=self.request.GET.get("q", ""))
