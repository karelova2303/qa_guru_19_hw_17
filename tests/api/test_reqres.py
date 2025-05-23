import requests
from jsonschema.validators import validate

from schemas import create_user, register_user, update_user
from tests.api.conftest import headers

endpoint_users = '/api/users/'
endpoint_register = '/api/register'


def test_get_list_users_on_page(url, headers):
    response = requests.get(f'{url}{endpoint_users}', params={"page": 2}, headers=headers)

    assert response.status_code == 200
    assert response.json()['per_page'] == 6


def test_get_single_user_not_found(url, headers):
    id = '23'
    response = requests.get(f'{url}{endpoint_users}{id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {}


def test_create_user(url, headers):
    name = "Jonny"
    job = "tester"

    payload = {
        "name": name,
        "job": job
    }
    response = requests.post(f'{url}{endpoint_users}', data=payload, headers=headers)

    assert response.status_code == 201
    body = response.json()
    validate(body, create_user)
    assert body['name'] == name
    assert body['job'] == job


def test_delete_user(url, headers):
    id = '3'
    response = requests.delete(f'{url}{endpoint_users}{id}', headers=headers)

    assert response.status_code == 204
    assert response.text == ''


def test_register_user_successfull(url, headers):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(f'{url}{endpoint_register}', data=payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    validate(body, register_user)
    assert body["id"] is not None


def test_register_user_unsuccessfull(url, headers):
    payload = {
        "email": "sydney@fife"
    }
    response = requests.post(f'{url}{endpoint_register}', json=payload, headers=headers)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_update_user(url, headers):
    name = 'Germiona'
    job = 'witch'
    id = '2'
    payload = {
        "name": name,
        "job": job
    }
    response = requests.put(f'{url}{endpoint_users}{id}', json=payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    validate(body, update_user)
    assert body['name'] == name
    assert body['job'] == job
