from django.db import models

# Create your models here.
class Tax(models.Model):
    idNumber = models.IntegerField(primary_key=True)
    parent = models.IntegerField(null=True)
    rank = models.CharField(max_length=30, null=True)
    sciName = models.CharField(max_length=30, null=True)
    comName = models.CharField(max_length=30, null=True)
    genComName = models.CharField(max_length=30, null=True)
    gcID = models.IntegerField(null=True)
    mgcID = models.IntegerField(null=True)
    def __str__(self):
        return(self.sciName)


class Names(models.Model):
    altName = models.CharField(max_length=30)
    idNumber = models.IntegerField()
    def __str__(self):
        return(self.idNumber)
