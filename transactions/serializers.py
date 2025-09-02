from rest_framework import serializers
from .models import Category, Transaction, MonthlySummary

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_type = serializers.CharField(source='category.type', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'category', 'category_name', 'category_type', 'amount', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description', 'date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MonthlySummarySerializer(serializers.ModelSerializer):
    month_display = serializers.CharField(source='month.strftime', read_only=True)

    class Meta:
        model = MonthlySummary
        fields = ['id', 'month', 'month_display', 'total_income', 'total_expenses', 'balance', 'created_at']
        read_only_fields = ['id', 'created_at']