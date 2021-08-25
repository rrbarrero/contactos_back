from django_filters import rest_framework as filters
from agenda.models import Cargo


class CargoFilter(filters.Filter):
    cargo = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Cargo
        fields = ["colectivo", "subcolectivo"]
