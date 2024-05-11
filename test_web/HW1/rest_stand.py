import requests
import yaml
with open("config.yaml") as f:
    data = yaml.safe_load(f)


def test_step1(login, testtext1):
    header = {"X-Auth-Token": login}
    res = requests.get(data["site"] + "api/posts", params={"owner": "notMe"}, headers=header)
    listres = [i["title"] for i in res.json()["data"]]
    assert testtext1 in listres

def test_step2(login, testtext2):
    header = {"X-Auth-Token": login}
    requests.post(data["site"] + "api/posts", data={"title": "testPost", "description": "test_post_PY", "content": "content for testing from PY"}, headers=header)
    res = requests.get(data["site"] + "api/posts", params={"owner": "me"}, headers=header)
    listres = [i["description"] for i in res.json()["data"]]
    assert testtext2 in listres

