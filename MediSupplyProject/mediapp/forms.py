from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, OrderItem

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['status']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['description', 'quantity', 'price']


# Inline formset: ties OrderItem to its PurchaseOrder
OrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    OrderItem,
    form=OrderItemForm,
    extra=1,          # render one blank row by default
    can_delete=True   # allow removing items
)