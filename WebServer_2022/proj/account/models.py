from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    DisableList = models.TextField(default='""')
    AvailableList = models.TextField(default='""')
    Default_Access = models.BooleanField(null=True)
  
    def __str__(self):
        return self.username
