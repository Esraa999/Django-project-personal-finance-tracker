from django.contrib import admin

# Register your models here.
from .models import Category, Transaction, MonthlySummary

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date', 'created_at')
    list_filter = ('category__type', 'category', 'date', 'created_at')
    search_fields = ('user__username', 'description', 'category__name')
    date_hierarchy = 'date'
    raw_id_fields = ('user',)

@admin.register(MonthlySummary)
class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'total_income', 'total_expenses', 'balance')
    list_filter = ('month', 'created_at')
    search_fields = ('user__username',)
    date_hierarchy = 'month'
    raw_id_fields = ('user',)