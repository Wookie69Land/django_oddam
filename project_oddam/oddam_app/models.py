from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.exceptions import PermissionDenied

from django_currentuser.middleware import get_current_authenticated_user


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'Donation nr {self.id} for {self.institution}'


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    superusers = User.objects.filter(is_superuser=True)
    if instance.is_superuser:
        if superusers.count() == 1:
            raise PermissionDenied("Nie możesz skasować ostatniego superusera")
        if get_current_authenticated_user() == instance:
            raise PermissionDenied("Nie możesz skasować samego siebie")

