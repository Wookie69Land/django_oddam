import pytest

from django.shortcuts import reverse

from .testutils import *


@pytest.mark.django_db
def test_user_creation(client, set_up):
    users_count = count_users()
    user = create_superuser()
    client.login(username=user.username, password='FakeFake69@')
    assert count_users() == users_count + 1


@pytest.mark.django_db
def test_landing(client, set_up):
    url = reverse('start')
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_donation_page(client, set_up):
#     user = create_superuser()
#     client.login(username=user.username, password='FakeFake69@')
#     url_reverse = reverse('donation', {})
#     response = client.post(url_reverse)
#     assert response.status_code == 200


