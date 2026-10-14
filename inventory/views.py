from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.db import transaction
from .models import Product, Category, Supplier, StockTransaction
from .forms import ProductForm, StockTransactionForm, SupplierForm

def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    low_stock_products = Product.objects.filter(
        quantity__lte=5
    ).count()

    inventory_value = sum(
        product.quantity * product.price
        for product in Product.objects.all()
    )

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_products': low_stock_products,
        'inventory_value': inventory_value,
    }

    return render(request, 'inventory/dashboard.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'inventory/add_product.html', {'form': form})


def product_list(request):
    products = Product.objects.select_related(
        'category', 'supplier'
    ).all().order_by('name')

    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all().order_by('name')

    return render(
        request,
        'inventory/product_list.html',
        {
            'products': products,
            'search_query': search_query,
            'categories': categories,
            'selected_category': category_id,
        }
    )


def low_stock_list(request):
    products = Product.objects.filter(
        quantity__lte=F('minimum_stock')
    ).select_related(
        'category', 'supplier'
    ).order_by('quantity')

    return render(
        request,
        'inventory/low_stock.html',
        {'products': products}
    )

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'inventory/edit_product.html',
        {
            'form': form,
            'product': product,
        }
    )

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(
        request,
        'inventory/delete_product.html',
        {'product': product}
    )

def manage_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = StockTransactionForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            transaction_type = form.cleaned_data['transaction_type']

            with transaction.atomic():
                product = Product.objects.select_for_update().get(
                    id=product_id
                )

                if (
                    transaction_type == 'OUT'
                    and quantity > product.quantity
                ):
                    form.add_error(
                        'quantity',
                        f'Insufficient stock! Only {product.quantity} '
                        f'units are available.'
                    )
                else:
                    if transaction_type == 'IN':
                        product.quantity += quantity
                    else:
                        product.quantity -= quantity

                    product.save(update_fields=['quantity'])

                    stock_transaction = form.save(commit=False)
                    stock_transaction.product = product
                    stock_transaction.save()

                    return redirect('product_list')

    else:
        form = StockTransactionForm()

    return render(
        request,
        'inventory/manage_stock.html',
        {
            'product': product,
            'form': form,
        }
    )

def stock_history(request):
    transactions = StockTransaction.objects.select_related(
        'product'
    ).order_by('-created_at')

    return render(
        request,
        'inventory/stock_history.html',
        {
            'transactions': transactions,
        }
    )


def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')

    return render(
        request,
        'inventory/supplier_list.html',
        {
            'suppliers': suppliers,
        }
    )

def add_supplier(request):

    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('supplier_list')

    else:
        form = SupplierForm()

    return render(
        request,
        'inventory/add_supplier.html',
        {
            'form': form,
        }
    )


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            return redirect('supplier_list')

    else:
        form = SupplierForm(instance=supplier)

    return render(
        request,
        'inventory/edit_supplier.html',
        {
            'form': form,
            'supplier': supplier,
        }
    )

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')

    return render(
        request,
        'inventory/delete_supplier.html',
        {'supplier': supplier}
    )