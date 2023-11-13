class OrderingMixin(object):
    ordering_fields = []

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", None)
        if ordering:
            ordering = [option for option in ordering.split(",") if option in self.ordering_fields]

        return ordering or super().get_ordering()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, ordering=self.get_ordering())
