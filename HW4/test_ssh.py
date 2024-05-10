from sshcheckers import ssh_checkout, upload_files, ssh_getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)

us = data["user"]
print(type(us))


def save_log(starttime, name):
    with open(name, "w") as file:
        file.write(ssh_getout(data["ip"], data["user"], data["passwd"], "journalctl --since'{}'".format(starttime)))


def test_step1(start_time):
    res = []
    upload_files(data["ip"], data["user"], data["passwd"], "/tests/" + data["pkgname"] + ".deb",
                 "/home/{}/{}.deb".format(data["user"], data["pkgname"]))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "echo {} | sudo -S dpkg -i /home/{}/{}.deb".format(data["passwd"], data["user"],
                                                                               data["pkgname"]), "Setting up"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "echo {} | sudo -S dpkg -s {}".format(data["passwd"], data["pkgname"]),
                            "Status: install ok installed"))
    save_log(start_time, "log1.txt")
    assert all(res), "test1 FAIL"


def test_step2(make_folders, clear_folders, make_files):
    # test2
    res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".
                        format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; ls".
                        format(data["folder_out"]), "arx2.7z")
    save_log(start_time, "log1.txt")
    assert res1 and res2, "test2 FAIL"


def test_step10(start_time):
    res = []
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "echo {} | sudo -S dpkg -r {}".format(data["passwd"], data["pkgname"]), "Removing"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "echo {} | sudo -S dpkg -s {}".format(data["passwd"], data["pkgname"]),
                            "Status: deinstall ok"))
    save_log(start_time, "log10.txt")
    assert all(res), "test10 FAIL"
