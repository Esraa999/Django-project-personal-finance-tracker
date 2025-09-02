from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from transactions.models import Category, Transaction
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Salary', 'type': 'income'},
            {'name': 'Freelance', 'type': 'income'},
            {'name': 'Investment Returns', 'type': 'income'},
            {'name': 'Groceries', 'type': 'expense'},
            {'name': 'Transportation', 'type': 'expense'},
            {'name': 'Utilities', 'type': 'expense'},
            {'name': 'Entertainment', 'type': 'expense'},
            {'name': 'Healthcare', 'type': 'expense'},
            {'name': 'Shopping', 'type': 'expense'},
            {'name': 'Dining Out', 'type': 'expense'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                type=cat_data['type']
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create test user if doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('Created test user: testuser/testpass123')

        # Create sample transactions for the last 3 months
        income_categories = Category.objects.filter(type='income')
        expense_categories = Category.objects.filter(type='expense')
        
        today = date.today()
        start_date = today - timedelta(days=90)
        
        transaction_count = 0
        current_date = start_date
        
        while current_date <= today:
            # Add some randomness to transaction creation
            if random.random() < 0.3:  # 30% chance of transaction each day
                # Random expense transaction
                if random.random() < 0.8:  # 80% chance expense
                    category = random.choice(expense_categories)
                    amount = Decimal(str(round(random.uniform(10, 300), 2)))
                    descriptions = {
                        'Groceries': ['Weekly groceries', 'Supermarket shopping', 'Fresh produce'],
                        'Transportation': ['Gas fill-up', 'Bus fare', 'Taxi ride', 'Uber trip'],
                        'Utilities': ['Electricity bill', 'Water bill', 'Internet bill'],
                        'Entertainment': ['Movie tickets', 'Concert', 'Netflix subscription'],
                        'Healthcare': ['Doctor visit', 'Pharmacy', 'Dental checkup'],
                        'Shopping': ['Clothes shopping', 'Amazon purchase', 'New shoes'],
                        'Dining Out': ['Restaurant dinner', 'Coffee shop', 'Fast food'],
                    }
                    description = random.choice(descriptions.get(category.name, ['Expense']))
                else:  # Income transaction
                    category = random.choice(income_categories)
                    if category.name == 'Salary':
                        amount = Decimal('3000.00')
                        description = 'Monthly salary'
                    else:
                        amount = Decimal(str(round(random.uniform(100, 1000), 2)))
                        description = f'{category.name} payment'
                
                Transaction.objects.create(
                    user=user,
                    category=category,
                    amount=amount,
                    description=description,
                    date=current_date
                )
                transaction_count += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {transaction_count} sample transactions'
            )
        )