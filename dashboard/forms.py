from django import forms 
from .models import GamingSession

class GamingSessionForm(forms.ModelForm):
    class Meta:
        model = GamingSession
        fields = [
            'date',
            'game_name',
            'start_balance',
            'end_balance',
            'spins',
            'bet',
            'best_win',
            'bonus_buy',
            'spin_mode',
        ]

