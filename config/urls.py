from django.contrib import admin
from django.urls import path
from inventory.views import (
    dashboard,
    add_product,
    product_list,
    low_stock_list,
    edit_product,
    delete_product,
    manage_stock,
    stock_history,
    supplier_list,
    add_supplier,
    edit_supplier,
    delete_supplier,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('products/add/', add_product, name='add_product'),
    path('products/', product_list, name='product_list'),
    path('low-stock/', low_stock_list, name='low_stock_list'),
    path('products/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('products/stock/<int:product_id>/', manage_stock, name='manage_stock'),
    path('stock-history/', stock_history, name='stock_history'),
    path('suppliers/', supplier_list, name='supplier_list'),
    path('suppliers/add/', add_supplier, name='add_supplier'),
    path('suppliers/edit/<int:supplier_id>/', edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:supplier_id>/', delete_supplier, name='delete_supplier'),
]