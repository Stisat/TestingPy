import time
from testpage import OperationsHelper
import logging
import yaml

with open("testdata.yaml") as f:
    data = yaml.safe_load(f)


def test_step1(browser):
    logging.info("Test1 Starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(data["username"])
    testpage.enter_pass("dsfdsf")
    testpage.click_login_btn()
    time.sleep(2)
    assert testpage.get_error_text() == "401"


def test_step2(browser):
    logging.info("Test2 Starting")
    testpage = OperationsHelper(browser)
    testpage.enter_login(data["username"])
    testpage.enter_pass(data["password"])
    testpage.click_login_btn()
    time.sleep(2)
    assert testpage.get_user_text() == f"Hello, {data["username"]}"


def test_step3(browser):
    logging.info("Test3 Starting")
    testpage = OperationsHelper(browser)
    testpage.click_new_post_btn()
    time.sleep(2)
    testpage.enter_title("test_title_new")
    testpage.enter_description("test_description")
    testpage.click_save_btn()
    time.sleep(3)
    assert testpage.get_res_text() == "test_title_new"


def test_step4(browser):
    logging.info("Test4 Starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.click_contact_as()
    testpage.enter_contact_name("Test_User_P6")
    testpage.enter_contact_email("sdfsdf@gmail.com")
    testpage.click_contact_us_btn()
    time.sleep(2)
    alert = browser.switch_to.alert
    text = alert.text
    assert text == "Form successfully submitted"
