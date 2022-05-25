from django import forms
from django.forms import TextInput, inlineformset_factory
from order.models import Order, OrderParticulars


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_address', 'customer_phone']
        widgets = {
            'customer_name': TextInput(attrs={'class':'form-control', 'placeholder':'Customer Name'}),
            'customer_address': TextInput(attrs={'class':'form-control', 'placeholder':'Customer Address'}),
            'customer_phone': TextInput(attrs={'class':'form-control', 'placeholder':'Customer Address'}),
        }

class OrderParticularsForm(forms.ModelForm):
    class Meta:
        model = OrderParticulars
        fields = ['order', 'item_name', 'price', 'quantity', 'total']

OrderParticularsFormset = inlineformset_factory(Order, OrderParticulars, form=OrderParticularsForm, extra=1)
