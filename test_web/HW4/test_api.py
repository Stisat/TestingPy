import requests
import yaml
import logging
from testpage import TestApi

with open("testdata.yaml") as f:
    data = yaml.safe_load(f)
login = TestApi().get_token_from_server()
test_text1 = "test"
test_text2 = "test_post_PY"

def test_step_api1():
    logging.info("Test_API1 Starting")
    header = {"X-Auth-Token": login}
    res = requests.get(data["address"] + "api/posts", params={"owner": "notMe"}, headers=header)
    listres = [i["title"] for i in res.json()["data"]]
    assert test_text1 in listres


def test_step_api2():
    logging.info("Test_API2 Starting")
    header = {"X-Auth-Token": login}
    requests.post(data["address"] + "api/posts", data={"title": "testPost", "description": "test_post_PY", "content": "content for testing from PY"}, headers=header)
    res = requests.get(data["address"] + "api/posts", params={"owner": "me"}, headers=header)
    listres = [i["description"] for i in res.json()["data"]]
    assert test_text2 in listres