from datetime import date
from django import forms
from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.core.exceptions import ValidationError

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class BookingForm(forms.ModelForm):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'num_adults', 'num_children']

    def clean(self):
        cleaned_data = super().clean()
        num_adults = cleaned_data.get('num_adults', 1)
        num_children = cleaned_data.get('num_children', 0)

        if num_adults < 1:
            raise forms.ValidationError("Number of adults must be at least 1.")

        if num_children < 0:
            raise forms.ValidationError("Number of children cannot be negative.")

        return cleaned_data
    
    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        today = date.today()

        # Check if check_in date is before today's date
        if check_in < today:
            raise ValidationError(
                ('Check-in date cannot be before today.'),
                code='invalid_check_in_date'
            )

        return check_in

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # Check if check_out is after check_in
        if check_in and check_out:
            if check_out <= check_in:
                raise ValidationError(
                    ('Check-out date must be after the check-in date.'),
                    code='invalid_dates'
                )

        return cleaned_data

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

    def clean_query(self):
        query = self.cleaned_data.get('query')
        if not query:
            raise forms.ValidationError("This field is required.")
        # Additional cleaning or validation can be done here
        return query
    
