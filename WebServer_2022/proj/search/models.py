from django.db import models
from search.utils.storage import OverwriteStorage


# Create your models here.
class T_H_Image(models.Model):
    image_name = models.CharField(max_length =128)
    image = models.ImageField(storage=OverwriteStorage(), upload_to='images/')
    
    def __str__(self):
        return self.image_name