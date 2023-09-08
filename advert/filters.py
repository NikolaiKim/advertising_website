import django_filters

from advert.models import Advert


# Модель для фильтрафии


class AdvertFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
    )

    # Фильтр, который позволяет искать совпадения в текстовых полях модели
    class Meta:
        model = Advert
        fields = ("title",)
