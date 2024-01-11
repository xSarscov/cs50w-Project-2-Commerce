from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from .models import Category

class CreateListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter a title',
        'aria-label': 'Enter a title',
        }))
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows': 3,
        'placeholder': 'Enter a description',
    }))

    image = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Paste the image URL'
    }))

    category = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    price = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter a price'
    }))

    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        choices = [(str(category.id), category.category_name) for category in categories]

        self.fields['category'].choices = choices