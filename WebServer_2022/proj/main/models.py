from django.db import models


# Create your models here.
class TaskResult(models.Model):
    pubDateTime = models.DateTimeField(auto_now_add=True)
    pubTime = models.CharField(max_length = 128, unique = True)
    original_result = models.TextField()
    devices_with_tableHTML = models.TextField()
    connectinIP = models.TextField() #dictionary in json
    IPPort = models.TextField() #list in json
    
    
    
    def __str__(self):
        return self.pubTime
    
#     class Meta:
#         ordering = ['pubDateTime']


# , default=str(int(time.time()))