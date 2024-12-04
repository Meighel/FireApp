from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from fire.models import Locations, Incident, FireStation, Firefighters, FireTruck, WeatherConditions
from django.forms.widgets import DateTimeInput
from datetime import datetime

class FireStationForm(forms.ModelForm):
    class Meta:
        model = FireStation
        fields = "__all__"

class FireTruckForm(forms.ModelForm):
    class Meta:
        model = FireTruck
        fields = "__all__"

class FireFighterForm(forms.ModelForm):
    class Meta:
        model = Firefighters
        fields = "__all__"

class LocationsForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = "__all__"

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = "__all__"

        widgets = {
            'date_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time and date_time > now():
            raise ValidationError("The date and time cannot be in the future.")
        return date_time
    
class WeatherConditionsForm(forms.ModelForm):
    class Meta:
        model = WeatherConditions
        fields = "__all__"