from django import forms
from django.utils import timezone

from .models import Customer, Reservation


class ReservationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = Reservation
        fields = ['table', 'date', 'start_time', 'end_time', 'guests']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        table = cleaned_data.get('table')
        guests = cleaned_data.get('guests')

        if date and date < timezone.localdate():
            self.add_error('date', 'Please choose today or a future date.')

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', 'End time must be after the start time.')

        if table and guests and guests > table.capacity:
            self.add_error('guests', f'This table can seat a maximum of {table.capacity} guests.')

        return cleaned_data

    def save(self, commit=True):
        customer, created = Customer.objects.get_or_create(
            email=self.cleaned_data['email'],
            defaults={
                'name': self.cleaned_data['name'],
                'phone': self.cleaned_data['phone'],
            },
        )
        reservation = super().save(commit=False)
        reservation.customer = customer
        if commit:
            reservation.save()
        return reservation
