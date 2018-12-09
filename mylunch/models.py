from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=30)
    age10 = models.DecimalField(max_digits=3, decimal_places=0)
    age20 = models.DecimalField(max_digits=3, decimal_places=0)
    age30 = models.DecimalField(max_digits=3, decimal_places=0)
    age40 = models.DecimalField(max_digits=3, decimal_places=0)
    age50 = models.DecimalField(max_digits=3, decimal_places=0)
    age60 = models.DecimalField(max_digits=3, decimal_places=0)
    female = models.DecimalField(max_digits=3, decimal_places=0)
    male = models.DecimalField(max_digits=3, decimal_places=0)
    rating = models.FloatField()
    category = models.DecimalField(max_digits=1, decimal_places=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)


