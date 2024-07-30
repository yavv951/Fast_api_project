from http import HTTPStatus

import requests

from tests.conftest import generate_data


def test_update_user(create_user, app_url):
    response = requests.get(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.OK
    user_data = generate_data()
    user_data['id'] = create_user
    response = requests.put(f"{app_url}/api/users/{create_user}", json=user_data)
    assert response.status_code == HTTPStatus.OK
    response = requests.delete(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.OK
    response = requests.get(f"{app_url}/api/users/{create_user}")
    assert response.status_code == HTTPStatus.NOT_FOUND
