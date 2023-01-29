import pytest

from django.shortcuts import reverse
from django.db.models import Sum, Count
from django.core import mail

from datetime import datetime, date

from .testutils import *


@pytest.mark.django_db
def test_user_creation(client, set_up):
    users_count = count_users()
    user = create_superuser()
    client.login(username=user.username, password='FakeFake69@')
    assert count_users() == users_count + 1


@pytest.mark.django_db
def test_landing(client, set_up):

    bags = Donation.objects.aggregate(Sum('quantity'))
    bags = bags['quantity__sum']
    institutions = Donation.objects.values('institution').distinct().count()

    url = reverse('start')
    response = client.get(url)
    assert response.status_code == 200
    assert bags == response.context['bags']
    assert institutions == response.context['institutions']


@pytest.mark.django_db
def test_donation_page(client, set_up):
    user = create_superuser()
    client.login(username=user.username, password='FakeFake69@')
    institution = random_institution()
    url_reverse = reverse('donation')
    response = client.post(url_reverse, {
        'categories': '1',
        'bags': '69',
        'organization': institution.id,
        'address': 'Street',
        'city': 'City',
        'postcode': '00-000',
        'phone': '111222333',
        'data': str(date.today()),
        'time': str(datetime.now().strftime("%H:%M")),
        'more_info': ''
    })
    donation = Donation.objects.all().last()
    assert response.status_code == 302
    assert 'Street' == donation.address
    assert '111222333' == donation.phone_number
    assert 69 == donation.quantity


@pytest.mark.django_db
def test_send_report(client, set_up):
    user = create_superuser()
    url = reverse('forgotten-password')
    response = client.post(url, {'email': user.email})
    print(response.context)
    assert response.status_code == 200
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == 'Reset hasła'
    assert list(email.to) == [user.email]


