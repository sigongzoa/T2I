from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

class tblDemograph(models.Model):
    dbID = models.CharField(max_length=12,primary_key=True,unique=True)
    NoDemo = models.DecimalField(max_digits=10, decimal_places=0)
    Hospital = models.DecimalField(max_digits=1, decimal_places=0)
    DoB = models.DateField()
    Sex = models.DecimalField(max_digits=1,decimal_places=0)
    Marital_Status = models.DecimalField(max_digits=1, decimal_places=0)
    Rehab_Setting = models.DecimalField(max_digits=1, decimal_places=0)