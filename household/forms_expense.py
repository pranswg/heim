from django import forms
from .models import OutOfPocketTransaction

class ExpenseTransactionForm(forms.ModelForm):
    class Meta:
        model = OutOfPocketTransaction
        fields = ['item_name', 'amount', 'payment_method', 'category']
        labels = {
            'item_name': 'Purchased Item / Service Name',
            'amount': 'Total Cost (in local currency)',
            'payment_method': 'Mode of Payment',
            'category': 'Expense Category Group',
        }