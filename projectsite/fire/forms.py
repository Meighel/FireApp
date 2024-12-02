from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from fire.models import Locations, Incident, FireStation, Firefighters, FireTruck, WeatherConditions
from django.forms.widgets import DateTimeInput
from datetime import datetime

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = "__all__"

        widgets = {
            'date_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class WeatherConditionsForm(forms.ModelForm):
    class Meta:
        model = WeatherConditions
        fields = "__all__"