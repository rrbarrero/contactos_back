from django_filters import rest_framework as filters
from agenda.models import Cargo


class CargoFilter(filters.FilterSet):
    cargo = filters.CharFilter(lookup_expr="iexact")
    # colectivo = filters.NumberFilter(field_name="colectivo[]", lookup_expr="in")
    # colectivo = filters.NumberFilter(method="colectivo_filter_in")
    # subcolectivo = django_filters.NumberFilter(
    #     field_name="subcolectivo", lookup_expr="in"
    # )

    class Meta:
        model = Cargo
        fields = [
            "cargo",
        ]

