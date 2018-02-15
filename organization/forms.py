from django import forms
from .models import *

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        exclude = ['created_at', 'last_sync_at', 'repositories_json', 'slug', 'updated_at']
        widgets = {
            'description': forms.Textarea(),
        }

class RepositoriesSearchForm(forms.Form):
    order_by_choices = [
        ("created_at", "Created At"),
        ("updated_at", "Last Update"),
    ]

    name = forms.CharField(required=False, label="Name")
    order_by = forms.ChoiceField(choices=order_by_choices, label="Order By")

    def __init__(self, *args, **kwargs):
        super(RepositoriesSearchForm, self).__init__(*args, **kwargs)
