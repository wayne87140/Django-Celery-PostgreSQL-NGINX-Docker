from django.db import models
from account.models import User


# Create your models here.
class FavoriteDevice(models.Model):
    IPlikes = models.ManyToManyField(User)
    device_IP = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.device_IP