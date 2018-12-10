from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.DecimalField(max_digits=1, decimal_places=0)
    age = models.DecimalField(max_digits=3, decimal_places=0)
    category1 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    category2 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    category3 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    category4 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    category5 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    price1 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    price2 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    price3 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    price4 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    distance1 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    distance2 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    distance3 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    distance4 = models.DecimalField(max_digits=4, decimal_places=0, default=10)
    distance5 = models.DecimalField(max_digits=4, decimal_places=0, default=10)