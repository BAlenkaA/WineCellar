import django_filters

from .models import Vine, Variety, Category, Sweetness, Color


class VineFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    variety = django_filters.ModelMultipleChoiceFilter(queryset=Variety.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    colors = django_filters.ModelChoiceFilter(queryset=Color.objects.all())
    sweetness = django_filters.ModelChoiceFilter(queryset=Sweetness.objects.all())
    factory = django_filters.CharFilter(lookup_expr='icontains', label='Завод изготовителя')
    tasty = django_filters.BooleanFilter()

    class Meta:
        model = Vine
        fields = ['title', 'variety', 'category', 'colors', 'sweetness', 'factory', 'tasty']