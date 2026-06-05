from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InventoryItem
from .forms import InventoryItemForm
from .models import RequestItem
from .forms import RequestItemForm
from .models import OutOfPocketTransaction
from .forms_expense import ExpenseTransactionForm
from django.db.models import Sum

class HomePageView(ListView):
    model = InventoryItem
    context_object_name = 'inventory_items'
    template_name = "home.html" # Connects directly to our global template blueprint

class InventoryListView(ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'inventory_items'
    paginate_by = 5  # Keeps page lengths managed as required by your layout specs

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(item_name__icontains=query)
        return queryset.order_by('item_name')

# 2. CREATE: Form view to add a new inventory item
class InventoryCreateView(CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory-list')

# 3. UPDATE: Form view to modify stock numbers or units
class InventoryUpdateView(UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory-list')

# 4. DELETE: Confirmation screen before removing an item
class InventoryDeleteView(DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')

# 1. READ: Display a searchable, paginated queue of requests
class RequestListView(ListView):
    model = RequestItem
    template_name = 'requests/request_list.html'
    context_object_name = 'request_items'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(item_name__icontains=query)
        return queryset.order_by('-created_at') # Newest requests appear at the top

# 2. CREATE: Submit a new request
class RequestCreateView(CreateView):
    model = RequestItem
    form_class = RequestItemForm
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request-list')

    def form_valid(self, form):
        # Automatically assign the request to the currently logged-in user if authenticated
        if self.request.user.is_authenticated:
            form.instance.requester = self.request.user
        else:
            from django.contrib.auth.models import User
            form.instance.requester = User.objects.first() # Safe backup for local evaluation
        return super().form_valid(form)

# 3. UPDATE: Edit urgency, status, or description parameters
class RequestUpdateView(UpdateView):
    model = RequestItem
    form_class = RequestItemForm
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request-list')

# 4. DELETE: Pull a request from the tracking log
class RequestDeleteView(DeleteView):
    model = RequestItem
    template_name = 'requests/request_confirm_delete.html'
    success_url = reverse_lazy('request-list')

# 1. READ: List all expenses with search and a dynamic sum calculation summary card
class ExpenseListView(ListView):
    model = OutOfPocketTransaction
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(item_name__icontains=query)
        return queryset.order_by('-transaction_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate the grand total of all matching expenses dynamically
        filtered_qs = self.get_queryset()
        context['grand_total'] = filtered_qs.aggregate(Sum('amount'))['amount__sum'] or 0.00
        return context

# 2. CREATE: Record a new outlay receipt
class ExpenseCreateView(CreateView):
    model = OutOfPocketTransaction
    form_class = ExpenseTransactionForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.payer = self.request.user
        else:
            from django.contrib.auth.models import User
            form.instance.payer = User.objects.first()
        return super().form_valid(form)

# 3. UPDATE: Modify a price adjustment or payment label
class ExpenseUpdateView(UpdateView):
    model = OutOfPocketTransaction
    form_class = ExpenseTransactionForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

# 4. DELETE: Wipe a bad receipt ledger entry
class ExpenseDeleteView(DeleteView):
    model = OutOfPocketTransaction
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')