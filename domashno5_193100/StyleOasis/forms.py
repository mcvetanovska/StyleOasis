from django import forms
from .models import Item

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'category', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
