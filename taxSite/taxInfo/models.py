from django.db import models

# Create your models here.
class Tax(models.Model):
    idNumber = models.IntegerField(primary_key=True)
    parent = models.IntegerField()
    rank = models.CharField(max_length=30)
    sciName = models.CharField(max_length=30)
    comName = models.CharField(max_length=30)
    genComName = models.CharField(max_length=30)
    gcID = models.IntegerField()
    mgcID = models.IntegerField()
    def __str__(self):
        return(self.sciName)


class Names(models.Model):
    altName = models.CharField(max_length=30)
    idNumber = models.IntegerField()
    def __str__(self):
        return(self.altName)
