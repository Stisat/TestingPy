import yaml
import pytest

with open("testdata.yaml") as f:
    test_data = yaml.safe_load(f)


@pytest.fixture()
def x_selector1():
    return """//*[@id="login"]/div[1]/label/input"""


@pytest.fixture()
def x_selector2():
    return """//*[@id="login"]/div[2]/label/input"""


@pytest.fixture()
def x_selector3():
    return """//*[@id="app"]/main/div/div/div[2]/h2"""


@pytest.fixture()
def btn_selector():
    return """button"""


@pytest.fixture()
def er1():
    return "401"

@pytest.fixture()
def enter_site_selector():
    return """//*[@id="app"]/main/nav/ul/li[3]/a"""

@pytest.fixture()
def welcome():
    return "Hello, {}".format(test_data["username"])


@pytest.fixture()
def add_post_selector():
    return """//*[@id="create-btn"]"""

@pytest.fixture()
def title_post_selector():
    return """//*[@id="create-item"]/div/div/div[1]/div/label/input"""

@pytest.fixture()
def save_button_selector():
    return """//*[@id="create-item"]/div/div/div[7]/div/button"""

@pytest.fixture()
def new_post_selector():
    return """h1"""


@pytest.fixture()
def post_name():
    return "test_PY_new"