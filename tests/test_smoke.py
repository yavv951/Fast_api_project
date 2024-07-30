import requests
from http import HTTPStatus
import pytest

from models.AppStatus import AppStatus


@pytest.mark.smoke
def test_service_is_up(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK
    status = AppStatus.model_validate(response.json())
    assert status.database is True
    assert response.headers["content-type"] == "application/json"