from django import forms
from .models import GamingSession

class GamingSessionForm(forms.ModelForm):
    class Meta:
        model = GamingSession
        exclude = ['profit']
