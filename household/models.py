from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# for Inventory Item Table
class InventoryItem(BaseModel):
    item_name = models.CharField(max_length=150)
    current_stock = models.IntegerField(default=0)
    min_stock_threshold = models.IntegerField(default=2)
    unit = models.CharField(max_length=50, default="pieces")

    def __str__(self):
        return f"{self.item_name} ({self.current_stock} {self.unit} left)"

# for Expense Log Table
class Expense(BaseModel):
    CATEGORY_CHOICES = [
        ('Groceries', 'Groceries'),
        ('Medical', 'Medical'),
        ('Utilities', 'Utilities'),
        ('Personal Care', 'Personal Care'),
        ('Entertainment', 'Entertainment'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.buyer.username} spent ${self.amount} on {self.category}"

# for Request Item Table
class RequestItem(BaseModel):
    URGENCY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    STATUS_CHOICES = [('Pending', 'Pending'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    item_name = models.CharField(max_length=150)
    specification = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.CharField(max_length=50)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    associated_expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} requested by {self.requester.username} [{self.status}]"

class OutOfPocketTransaction(models.Model):
    CATEGORY_CHOICES = [
        ('Groceries', 'Groceries'),
        ('Medicines', 'Medicines & Medical'),
        ('Utilities', 'Utilities & Bills'),
        ('Maintenance', 'Home Maintenance'),
        ('Other', 'Other Household Misc'),
    ]

    METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Digital Wallet', 'Digital Wallet / QR'),
    ]

    item_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Groceries')
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='Cash')
    
    # Automatically tracks who spent the money
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return f"{self.item_name} - ${self.amount} by {self.payer.username}"