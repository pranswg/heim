from django.contrib import admin
from .models import InventoryItem, Expense, RequestItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    # Enforces visual columns in your admin index dashboard
    list_display = ("item_name", "current_stock", "min_stock_threshold", "unit", "created_at")
    # Allows rapid real-time typing filters by text fields
    search_fields = ("item_name",)
    # Adds a sidebar drill-down filtering mechanism
    list_filter = ("unit", "created_at")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("buyer", "amount", "category", "description", "created_at")
    search_fields = ("description", "category", "buyer__username")
    list_filter = ("category", "created_at")

@admin.register(RequestItem)
class RequestItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "requester", "urgency", "status", "associated_expense", "created_at")
    search_fields = ("item_name", "specification", "requester__username")
    list_filter = ("urgency", "status", "created_at")