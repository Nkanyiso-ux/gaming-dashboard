from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GamingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    date = models.DateField()
    game_name = models.CharField(max_length=100)
    time_played = models.CharField(max_length=20)

    start_balance = models.FloatField()
    end_balance = models.FloatField()
    profit = models.FloatField(blank= True, null= True)

    spins = models.IntegerField()
    bet = models.FloatField()
    best_win = models.FloatField()

    bonus_buy = models.BooleanField(default=False)
    spin_mode = models.CharField(max_length=50)

    video_name = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        #Auto calculate profit
        self.profit = self.end_balance -self.start_balance
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.game_name} - {self.date}"
