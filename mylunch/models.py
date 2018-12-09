from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(primary_key=True, unique=True)
    age10 = models.DecimalField()
    age20 = models.DecimalField()
    age30 = models.DecimalField()
    age40 = models.DecimalField()
    age50 = models.DecimalField()
    age60 = models.DecimalField()
    female = models.DecimalField()
    male = models.DecimalField()
    rating = models.FloatField()
    category = models.DecimalField()
    price = models.DecimalField()


