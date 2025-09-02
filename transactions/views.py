from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.db.models import Q, Sum
from datetime import datetime, date
import csv
from .models import Category, Transaction, MonthlySummary
from .serializers import (
    CategorySerializer, 
    TransactionSerializer, 
    TransactionCreateUpdateSerializer,
    MonthlySummarySerializer
)
from .filters import TransactionFilter

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransactionFilter
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('category')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateUpdateSerializer
        return TransactionSerializer

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TransactionCreateUpdateSerializer
        return TransactionSerializer

class MonthlySummaryListView(generics.ListAPIView):
    serializer_class = MonthlySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MonthlySummary.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_transactions_csv(request):
    # Get query parameters for filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    
    # Build queryset
    queryset = Transaction.objects.filter(user=request.user).select_related('category')
    
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if category:
        queryset = queryset.filter(category_id=category)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Type', 'Amount', 'Description'])
    
    for transaction in queryset:
        writer.writerow([
            transaction.date,
            transaction.category.name,
            transaction.category.type,
            transaction.amount,
            transaction.description
        ])
    
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    # Get current month stats
    current_date = date.today()
    current_month_start = current_date.replace(day=1)
    
    current_month_transactions = Transaction.objects.filter(
        user=user,
        date__gte=current_month_start,
        date__month=current_date.month,
        date__year=current_date.year
    )
    
    total_income = current_month_transactions.filter(
        category__type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = current_month_transactions.filter(
        category__type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    balance = total_income - total_expenses
    
    return Response({
        'current_month': {
            'income': total_income,
            'expenses': total_expenses,
            'balance': balance,
            'transaction_count': current_month_transactions.count()
        }
    })