from django import forms
from django.forms import inlineformset_factory
from providers.models import Provider
from providers.utils.photo_utils import resize_photo
from services.models import Service


class ProviderFilterForm(forms.ModelForm):
    class Meta:
        model = Provider
        exclude = ("user", "photo", "thumbnail")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["description"].required = False
        self.fields["services"] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=Service.objects.values_list("pk", "title"),
        )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ("created_by",)


class ProviderForm(forms.ModelForm):
    services_formset = inlineformset_factory(Provider, Service, form=ServiceForm,
                                             fields=('title', 'description', 'price'), extra=1, can_delete=True)

    class Meta:
        model = Provider
        exclude = ['user', ]

    def clean_photo(self):
        photo_input = self.cleaned_data.get('photo')
        if photo_input:
            photo_input = resize_photo(photo_input, (140, 140))
        return photo_input

    def clean_thumbnail(self):
        thumbnail_input = self.cleaned_data.get('thumbnail')
        if thumbnail_input:
            thumbnail_input = resize_photo(thumbnail_input, (140, 140))
        return thumbnail_input
