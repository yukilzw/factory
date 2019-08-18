from django.db import models

class Company(models.Model):
    class Meta:
        db_table = 'user'
    id = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)