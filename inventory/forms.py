from django import forms
from .models import Product, StockTransaction, Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'supplier',
            'quantity',
            'price',
            'minimum_stock',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter product name'
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 0
            }),
            'price': forms.NumberInput(attrs={
                'min': 0,
                'step': '0.01'
            }),
            'minimum_stock': forms.NumberInput(attrs={
                'min': 0
            }),
        }


class StockTransactionForm(forms.ModelForm):

    class Meta:
        model = StockTransaction
        fields = ['transaction_type', 'quantity', 'note']

        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Enter quantity'
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reason for transaction (optional)'
            }),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is not None and quantity < 1:
            raise forms.ValidationError(
                'Quantity must be at least 1.'
            )

        return quantity

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier

        fields = [
            'name',
            'contact',
            'email',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier name'
            }),

            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact number'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
        }

