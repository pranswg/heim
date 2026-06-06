from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin

# Unified App Imports
from .models import InventoryItem, RequestItem, OutOfPocketTransaction
from .forms import InventoryItemForm, RequestItemForm
from .forms_expense import ExpenseTransactionForm

# ==============================================================================
# 1. CORE DASHBOARD / HUB
# ==============================================================================

class HomePageView(LoginRequiredMixin, ListView):
    model = InventoryItem
    context_object_name = 'inventory_items'
    template_name = "home.html"  # Connects directly to our global template blueprint


# ==============================================================================
# 2. SUPPLY INVENTORY TRACKER (MODULE: I)
# ==============================================================================

class InventoryListView(LoginRequiredMixin, ListView):
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


class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory-list')


class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory-list')


class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')


# ==============================================================================
# 3. TASK REQUEST QUEUE (MODULE: M)
# ==============================================================================

class RequestListView(LoginRequiredMixin, ListView):
    model = RequestItem
    template_name = 'requests/request_list.html'
    context_object_name = 'request_items'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(item_name__icontains=query)
        return queryset.order_by('-created_at')  # Newest requests appear at the top


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = RequestItem
    form_class = RequestItemForm
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request-list')

    def form_valid(self, form):
        # Automatically assign the request to the currently logged-in user
        if self.request.user.is_authenticated:
            form.instance.requester = self.request.user
        else:
            from django.contrib.auth.models import User
            form.instance.requester = User.objects.first()  # Safe backup for local evaluation
        return super().form_valid(form)


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = RequestItem
    form_class = RequestItemForm
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request-list')


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = RequestItem
    template_name = 'requests/request_confirm_delete.html'
    success_url = reverse_lazy('request-list')


# ==============================================================================
# 4. FINANCIAL LEDGER & SPLITTER (MODULE: E)
# ==============================================================================

class ExpenseListView(LoginRequiredMixin, ListView):
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


class ExpenseCreateView(LoginRequiredMixin, CreateView):
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


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = OutOfPocketTransaction
    form_class = ExpenseTransactionForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = OutOfPocketTransaction
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')