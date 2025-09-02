import django_filters
from .models import Transaction, Category

class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    category_type = django_filters.ChoiceFilter(
        field_name='category__type',
        choices=Category.CATEGORY_TYPES
    )
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date', 'category', 'category_type', 'amount_min', 'amount_max', 'description']