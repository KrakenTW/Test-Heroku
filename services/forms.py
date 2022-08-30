from django import forms

from services.models import Service
from providers.models import Provider


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["provider"].queryset = Provider.objects.filter(user=user)

    class Meta:
        model = Service
        exclude = ("created_by",)
