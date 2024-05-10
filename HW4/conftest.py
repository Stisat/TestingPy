import pytest
from sshcheckers import ssh_checkout, ssh_checkout_negative, ssh_getout, upload_files
import random
import string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture
def make_folders():
    return ssh_checkout(data["ip"], data["user"], data["passwd"], "mkdir {} {} {} {}".
                        format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture
def clear_folders():
    return ssh_checkout(data["ip"], data["user"], data["passwd"], "rm -rf {}/* {}/* {}/* {}/*".
                        format(data["folder_out"], data["folder_ext"], data["folder_in"], data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["ip"], data["user"], data["passwd"],
                        "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; mkdir {}".
            format(data["folder_in"], subfoldername), ""):
        return None, None
    elif not ssh_checkout(data["ip"], data["user"], data["passwd"],
                          "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".
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
    ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arxbad".
                 format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    ssh_checkout(data["ip"], data["user"], data["passwd"], "truncate -s 1 {}/arxbad.7z".
                 format(data["folder_out"]), "Everything is Ok")
    yield "arxbad"
    ssh_checkout(data["ip"], data["user"], data["passwd"], "rm -f {}/arxbad.7z".format(data["folder_out"]), "")


@pytest.fixture(autouse=True)
def add_statistic():
    stat_file = open("stat.txt", "a", encoding='utf-8')
    stat_file.write("Time: {}; File count: {}; File sizes: {}; Load: {}".
                    format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"],
                           ssh_getout(data["ip"], data["user"], data["passwd"], "cat /proc/loadavg")))
    stat_file.close()
