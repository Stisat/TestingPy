import pytest
import yaml
import requests

with open("config.yaml") as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def login():
    res1 = requests.post(data["site"] + "gateway/login", data={"username": data["username"], "password": data["password"]})
    print(res1.content)
    return res1.json()["token"]

@pytest.fixture()
def testtext1():
    return "test"


@pytest.fixture()
def testtext2():
    return "test_post_PY"