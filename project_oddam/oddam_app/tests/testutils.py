from random import sample, randint, choice
from django_faker import Faker

import random

from oddam_app.models import *


populator = Faker.getPopulator()


def populate_db():
    populator.addEntity(Category, 7)
    populator.addEntity(Institution, 20)
    populator.addEntity(Donation, 30)

    insertedPks = populator.execute()


def count_users():
    return User.objects.all().count()


def create_superuser():
    username = "Superuser"
    email = "superuser@fake.com"
    password = "FakeFake69@"
    person = User.objects.create_superuser(username=username,
                                           email=email,
                                           password=password)
    return person

