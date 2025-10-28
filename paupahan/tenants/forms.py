from django import forms
from django.utils import timezone
import calendar

from .models import Tenant, Charge, Payment


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ["name", "address", "date_started", "monthly_rent", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "autofocus": "autofocus", "placeholder": "Tenant full name"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Address or unit details"}),
            "date_started": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "monthly_rent": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ChargeForm(forms.ModelForm):
    # Build year and month choices dynamically
    _now_year = timezone.now().year
    YEAR_CHOICES = [(y, str(y)) for y in range(_now_year - 2, _now_year + 4)]
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]

    year = forms.TypedChoiceField(choices=YEAR_CHOICES, coerce=int, widget=forms.Select(attrs={"class": "form-select"}))
    month = forms.TypedChoiceField(choices=MONTH_CHOICES, coerce=int, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = Charge
        fields = ["tenant", "year", "month", "rent_amount", "water_charge", "electric_charge", "note"]
        widgets = {
            "tenant": forms.Select(attrs={"class": "form-select"}),
            "rent_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "water_charge": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "electric_charge": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["tenant", "charge", "amount", "date", "note"]
        widgets = {
            "tenant": forms.Select(attrs={"class": "form-select"}),
            "charge": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
