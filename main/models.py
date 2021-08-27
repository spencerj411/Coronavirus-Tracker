from django.db import models

# Create your models here.
class Confirmed(models.Model):
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2, default='00')
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_cases = models.IntegerField()

    def __str__(self):
        return self.province + ' ' + self.country + ': ' + str(self.num_cases)

# Create your models here.
class Deaths(models.Model):
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2, default='00')
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_cases = models.IntegerField()

    def __str__(self):
        return self.province + ' ' + self.country + ': ' + str(self.num_cases)