import time

import yaml
from module import Site

with open("testdata.yaml") as f:
    test_data = yaml.safe_load(f)

site = Site(test_data["address"])


def test_step1(x_selector1, x_selector2, x_selector3, btn_selector, er1):
    input1 = site.find_element("xpath", x_selector1)
    input1.send_keys("test")
    input2 = site.find_element("xpath", x_selector2)
    input2.send_keys("test")
    btn = site.find_element("css", btn_selector)
    btn.click()
    err_label = site.find_element("xpath", x_selector3)
    text = err_label.text
    site.close()
    assert text == er1


def test_step2(x_selector1, x_selector2, btn_selector, enter_site_selector, welcome):
    input1 = site.find_element("xpath", x_selector1)
    input1.clear()
    input1.send_keys(test_data["username"])
    input2 = site.find_element("xpath", x_selector2)
    input2.clear()
    input2.send_keys(test_data["password"])
    btn = site.find_element("css", btn_selector)
    btn.click()
    enter_label = site.find_element("xpath", enter_site_selector)
    text = enter_label.text
    site.close()
    assert text == welcome


def test_step3(x_selector1, x_selector2, btn_selector, add_post_selector, title_post_selector, save_button_selector, new_post_selector, post_name):
    input1 = site.find_element("xpath", x_selector1)
    input1.clear()
    input1.send_keys(test_data["username"])
    input2 = site.find_element("xpath", x_selector2)
    input2.clear()
    input2.send_keys(test_data["password"])
    btn = site.find_element("css", btn_selector)
    btn.click()
    add_btn = site.find_element("xpath", add_post_selector)
    add_btn.click()
    input3 = site.find_element("xpath", title_post_selector)
    input3.clear()
    input3.send_keys("test_PY_new")
    save_btn = site.find_element("xpath", save_button_selector)
    save_btn.click()
    time.sleep(test_data["sleep_time"])
    label_name = site.find_element("css", new_post_selector)
    text = label_name.text
    site.close()
    assert text == post_name


