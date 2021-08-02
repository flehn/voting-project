
from django import forms
from .models import Element


class CreateElementForm(forms.ModelForm):

    class Meta:
        model = Element
        fields = ['title', 'description', 'link']


