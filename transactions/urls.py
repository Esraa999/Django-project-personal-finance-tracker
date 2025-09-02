from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('monthly-summaries/', views.MonthlySummaryListView.as_view(), name='monthly-summary-list'),
    path('export-csv/', views.export_transactions_csv, name='export-csv'),
    path('dashboard/', views.dashboard_stats, name='dashboard'),
]