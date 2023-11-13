class SingleFilterMixin:
    filter_map = {}
    filtered_by_keys = None

    def get_queryset(self):
        queryset = super().get_queryset()
        keys = set(self.request.GET.keys()).intersection(set(self.filter_map.keys()))
        self.filtered_by_keys = keys
        for key in keys:
            query = self.filter_map[key]
            if not isinstance(query, dict):
                query = {query: self.request.GET[key]}
            queryset = queryset.filter(**query)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, filter_keys=list(self.filtered_by_keys))
