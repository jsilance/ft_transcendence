from django import forms
from .models import MapSettings, Shape

class PartyForm(forms.ModelForm):
    class Meta:
        model = MapSettings
        fields = ['nbPlayer', 'duringTime']
