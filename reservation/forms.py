import datetime

from django import forms
from django.utils.timezone import utc

from reservation.models import ReservationService


class ReservationServiceForm(forms.ModelForm):
    date = forms.DateTimeField(input_formats=['%I:%M %p %d-%b-%Y'],
                               widget=forms.DateTimeInput(
                                   attrs={'type': 'datetime-local'},
                                   format='%I:%M %p %d-%b-%Y'))

    def __init__(self, *args, **kwargs):
        super(ReservationServiceForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['service'].widget.attrs['readonly'] = True
        self.fields['reservation'].widget.attrs['readonly'] = True
        self.fields['reservation'].widget = forms.HiddenInput()

    def clean_date(self):
        choosen_date = self.cleaned_data['date']
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        is_reserved = ReservationService.objects.filter(date=choosen_date).exists()
        if is_reserved:
            self.add_error("date", "This date is already reserved. Please choose another one.")
            return None
        if choosen_date < now:
            self.add_error("date", "You can't book it in the past.")
            return None
        return choosen_date

    class Meta:
        model = ReservationService
        fields = ("service", "date", "price", "reservation",)
