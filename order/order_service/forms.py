from django import forms
from .models import Order, OrderedItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class OrderedItemForm(forms.ModelForm):
    class Meta:
        model = OrderedItem
        fields = ['product_id', 'quantity', 'status']
