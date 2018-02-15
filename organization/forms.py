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
        ("github_id", "Github ID"),
        ("-github_id", "Github ID - Desc"),
        ("github_created_at", "Created date on Github"),
        ("-github_created_at", "Created date on Github - Desc"),
        ("github_updated_at", "Last Update on Github"),
        ("-github_updated_at", "Last Update on Github - Desc"),
    ]

    name = forms.CharField(required=False, label="Name")
    order_by = forms.ChoiceField(choices=order_by_choices, label="Order By")

    def __init__(self, *args, **kwargs):
        super(RepositoriesSearchForm, self).__init__(*args, **kwargs)

    def get_valid_order_by_choices(self):
        return [choice for (choice, text) in self.order_by_choices]
