import json
from http import HTTPStatus

import pytest
import requests
from faker import Faker

from app.models.User import User
from tests.conftest import generate_data

faker = Faker()


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.mark.usefixtures("fill_test_data")
def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user(app_url):
    user_data = generate_data()
    response = requests.post(url=f"{app_url}/api/users/", json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    id_user = response.json().get("id")
    response = requests.get(f"{app_url}/api/users/{id_user}")
    assert response.status_code == HTTPStatus.OK


def test_update_user(create_user, app_url):
    user_data = generate_data()
    user_data['id'] = create_user
    response = requests.patch(f"{app_url}/api/users/{create_user}", json=user_data)
    assert response.status_code == HTTPStatus.OK


def test_update_user_without_id(app_url):
    user_data = generate_data()
    response = requests.patch(f"{app_url}/api/users/{9999999999}", json=user_data)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_not_allowed_metod(app_url, create_user):
    user_data = generate_data()
    response = requests.patch(f"{app_url}/api/users/{create_user}", json=user_data)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_delete_user(create_user, app_url):
    response = requests.get(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.OK
    response = requests.delete(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.OK
    response = requests.get(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_not_allowed_metod(create_user, app_url):
    response = requests.get(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.OK
    response = requests.put(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_delete_user_without_id(app_url):
    response = requests.delete(f"{app_url}/api/users/{9999999999}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("value", ['email', 'first_name', 'last_name', 'avatar'])
def test_update_user_invalid_data(create_user, app_url, value):
    user_data = generate_data()
    user_data[value] = 2
    response = requests.put(f"{app_url}/api/users/{create_user}", json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("value", ['email', 'first_name', 'last_name', 'avatar'])
def test_create_user_invalid_data(app_url, value):
    user_data = generate_data()
    user_data[value] = 2
    response = requests.post(url=f"{app_url}/api/users/", json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("value", ['email', 'first_name', 'last_name', 'avatar'])
def test_update_user_without_value_data(create_user, app_url, value):
    user_data = generate_data()
    del user_data[value]
    response = requests.patch(f"{app_url}/api/users/{create_user}", json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("value", ['email', 'first_name', 'last_name', 'avatar'])
def test_create_user_without_value_data(app_url, value):
    user_data = generate_data()
    del user_data[value]
    response = requests.post(url=f"{app_url}/api/users/", json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("value", ['', {}])
def test_update_user_without_data(create_user, app_url, value):
    user_data = value
    response = requests.patch(f"{app_url}/api/users/{create_user}", json=user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("value", ['', {}])
def test_create_user_without_data(app_url, value):
    user_data = value
    response = requests.post(url=f"{app_url}/api/users/", json=user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
