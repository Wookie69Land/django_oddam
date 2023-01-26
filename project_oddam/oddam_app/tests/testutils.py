from random import sample, randint, choice
from faker import Faker, Factory

import random

from oddam_app.models import *


faker = Faker('pl')


def populate_db():
    fake = Factory.create("pl")
    i = random.randint(10, 25)
    for _ in range(1, i):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = first_name + last_name + str(random.randint(1, 666)) + '@gmail.com'
        User.objects.create_user(username=email,
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email)

    j = random.randint(5, 9)
    for number in range(1, j):
        Category.objects.create(name=f"Category{number}")

    k = random.randint(10, 20)
    for number in range(1, k):
        institution = Institution()
        institution.name = f'Institution{number}'
        institution.description = fake.sentence()
        institution.type = random.choice(INST_TYPE)[0]
        institution.save()
        for _ in range(1, 3):
            categories = Category.objects.all()
            cat = random.choice(categories)
            institution.categories.add(cat.id)

    for number in range(10, 20):
        donation = Donation()
        donation.quantity = random.randint(1, 10)
        donation.institution = random.choice(Institution.objects.all())
        donation.address = f'Street{number}'
        donation.phone_number = fake.phone_number()
        donation.city = f'City{number}'
        donation.zip_code = f'{number}0-000'
        donation.pick_up_date = fake.date()
        donation.pick_up_time = fake.time()
        donation.pick_up_comment = f'{number}'
        donation.is_taken = random.choice([True, False])
        donation.user = random.choice(User.objects.all())
        donation.save()
        for _ in range(1, 3):
            categories = Category.objects.all()
            cat = random.choice(categories)
            donation.categories.add(cat.id)


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


def random_user():
    users = User.objects.all()
    return choice(users)

