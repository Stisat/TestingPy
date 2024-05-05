import pytest
from checkers import checkout, checkout_negative, getout
import random
import string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture
def make_folders():
    return checkout(
        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_out"], data["folder_ext"], data["folder_in"],
                                                        data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".
                            format(data["folder_in"], filename), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    elif not checkout("cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".
                              format(data["folder_in"], subfoldername, testfilename, data["bs"]), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def damage_file():
    checkout("cd {}; 7z a {}/arxbad".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    checkout("truncate -s 1 {}/arxbad.7z".format(data["folder_out"]), "Everything is Ok")
    yield "arxbad"
    checkout("rm -f {}/arxbad.7z".format(data["folder_out"]), "")


@pytest.fixture(autouse=True)
def add_statistic():
    stat_file = open("stat.txt", "a", encoding='utf-8')
    stat_file.write("Time: {}; File count: {}; File sizes: {}; Load: {}".
                    format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"],
                           getout("cat /proc/loadavg")))
    stat_file.close()
