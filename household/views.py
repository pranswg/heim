from django.views.generic.list import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InventoryItem
from .forms import InventoryItemForm

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