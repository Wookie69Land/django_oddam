from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


INST_TYPE = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
)


class Institution(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    type = models.SmallIntegerField(choices=INST_TYPE, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=8)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

