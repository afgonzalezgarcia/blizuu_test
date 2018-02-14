from django import forms
from .models import *

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        exclude = ['created_at', 'last_sync_at', 'repositories_json', 'slug', 'updated_at']
        widgets = {
            'description': forms.Textarea(),
        }
