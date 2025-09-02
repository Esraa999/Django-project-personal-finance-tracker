from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Sum
from datetime import date, datetime
from transactions.models import Transaction, MonthlySummary

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate monthly summaries for all users'

    def handle(self, *args, **options):
        current_date = date.today()
        # Generate for previous month
        if current_date.month == 1:
            month = 12
            year = current_date.year - 1
        else:
            month = current_date.month - 1
            year = current_date.year
        
        summary_date = date(year, month, 1)
        
        users = User.objects.all()
        created_count = 0
        updated_count = 0
        
        for user in users:
            # Get transactions for the month
            transactions = Transaction.objects.filter(
                user=user,
                date__year=year,
                date__month=month
            )
            
            if not transactions.exists():
                continue
            
            # Calculate totals
            income_total = transactions.filter(
                category__type='income'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            expense_total = transactions.filter(
                category__type='expense'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Create or update monthly summary
            summary, created = MonthlySummary.objects.get_or_create(
                user=user,
                month=summary_date,
                defaults={
                    'total_income': income_total,
                    'total_expenses': expense_total,
                }
            )
            
            if not created:
                summary.total_income = income_total
                summary.total_expenses = expense_total
                summary.save()
                updated_count += 1
            else:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated monthly summaries. Created: {created_count}, Updated: {updated_count}'
            )
        )