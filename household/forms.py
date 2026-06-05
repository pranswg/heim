from django import forms
from .models import InventoryItem

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