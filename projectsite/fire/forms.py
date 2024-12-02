from django.forms import ModelForm
from django import forms
from fire.models import Locations, Incident, FireStation, Firefighters, FireTruck, WeatherConditions

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = "__all__"

        widgets = {
            'date_time' : forms.DateInput(attrs={'type': 'date'})
        }