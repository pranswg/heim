from django import forms
from .models import InventoryItem
from .models import RequestItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'current_stock', 'min_stock_threshold', 'unit']
        # Adding labels for clean UI rendering
        labels = {
            'item_name': 'Item Name',
            'current_stock': 'Current Quantity',
            'min_stock_threshold': 'Low Stock Alert Threshold',
            'unit': 'Unit of Measurement (e.g., eggs, liters, packs)',
        }

class RequestItemForm(forms.ModelForm):
    class Meta:
        model = RequestItem
        fields = ['item_name', 'specification', 'quantity', 'urgency', 'status', 'associated_expense']
        labels = {
            'item_name': 'Requested Item Name',
            'specification': 'Specification / Details (e.g., "500mg, Non-drowsy")',
            'quantity': 'Quantity Needed (e.g., "2 packs", "1 bottle")',
            'urgency': 'Urgency Level',
            'status': 'Processing Status',
            'associated_expense': 'Link to Expense Record (Optional)',
        }