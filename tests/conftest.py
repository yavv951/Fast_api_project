import logging
import os

import dotenv
import pytest
import requests

from app.models.User import UserCreate
from faker import Faker
import random

faker = Faker()


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")

    # return user_data.model_dump(mode='json')


def generate_data():
    image_id = random.randint(1, 12)
    user_data = UserCreate(email=faker.email(),
                           first_name=faker.first_name(),
                           last_name=faker.last_name(),
                           avatar=f"https://reqres.in/img/faces/{image_id}-image.jpg"
                           )
    return user_data.model_dump(mode='json')


@pytest.fixture()
def create_user(app_url):
    user_data = generate_data()
    response = requests.post(url=f"{app_url}/api/users/", json=user_data)
    response.raise_for_status()
    user_id = response.json().get("id")
    yield user_id
    requests.delete(f"{app_url}/api/users/{user_id}")
