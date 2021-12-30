from django import forms
from django.core.exceptions import ValidationError

from .models import CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = [
            'quantity'
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0 or quantity > 25:
            raise ValidationError("Quantity error")
        return quantity
