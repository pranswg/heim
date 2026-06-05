"""
URL configuration for household project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    HomePageView, 
    InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView,
    RequestListView, RequestCreateView, RequestUpdateView, RequestDeleteView,
    ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    
    # Core Authentication routing loop matching allauth criteria
    path('accounts/', include('allauth.urls')),
    
    # Inventory CRUD
    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/new/', InventoryCreateView.as_view(), name='inventory-create'),
    path('inventory/<int:pk>/edit/', InventoryUpdateView.as_view(), name='inventory-edit'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory-delete'),
    
    # Request Queues CRUD
    path('requests/', RequestListView.as_view(), name='request-list'),
    path('requests/new/', RequestCreateView.as_view(), name='request-create'),
    path('requests/<int:pk>/edit/', RequestUpdateView.as_view(), name='request-edit'),
    path('requests/<int:pk>/delete/', RequestDeleteView.as_view(), name='request-delete'),
    
    # Expense Matrix CRUD Routing Loop
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/new/', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense-edit'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
]