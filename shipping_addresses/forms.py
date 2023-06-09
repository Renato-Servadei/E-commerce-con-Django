from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model=ShippingAddress   
        fields=[
            'line1', 'line2','city', 'state', 'country', 'postal_code', 'reference'
        ]
        labels = {
            'line1': 'Calle 1', 
            'line2' : 'Calle 2',
            'city': 'Ciudad', 
            'state': 'Provincia',
            'country': 'País', 
            'postal_code': 'Código Postal', 
            'reference': 'Referencia'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['line1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['line2'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['state'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['postal_code'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'C1431HTD'
        })
        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
        })