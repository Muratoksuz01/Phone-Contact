from .models import ContactBook
from django import forms

class ContactBookForm(forms.ModelForm):

    class Meta:
        model=ContactBook
        fields=("image","mobile_phone","email","label","person_name")