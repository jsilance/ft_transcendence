from django import forms
from .models import MapSettings

class PartyForm(forms.ModelForm):
    class Meta:
        model = MapSettings
        fields = ['duringTime']
