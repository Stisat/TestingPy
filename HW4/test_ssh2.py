from sshcheckers import ssh_checkout, ssh_getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def save_log(starttime, name):
    with open(name, "w") as file:
        file.write(ssh_getout(data["ip"], data["user"], data["passwd"], "journalctl --since'{}'".format(starttime)))


def test_step1(make_folders, clear_folders, make_files):
    # test1
    res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".
                        format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; ls".
                        format(data["folder_out"]), "arx2.7z")
    assert res1 and res2, "test1 FAIL"


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".
                            format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z e arx2.7z -o{} -y".
                            format(data["folder_out"], data["folder_ext"]), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext"]), item))
    assert all(res), "test2 FAIL"


def test_step3():
    # test3
    assert ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z t arx2.7z".
                        format(data["folder_out"]), "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z u arx2.7z".
                        format(data["folder_out"]), "Everything is Ok"), "test4 FAIL"


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".
                            format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z l arx2.7z".
                                format(data["folder_out"]), item))
    assert all(res), "test5 FAIL"


def test_step6(clear_folders, make_files, make_subfolder):
    # test6
    res = []
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx".
                            format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z x arx.7z -o/{} -y".
                            format(data["folder_out"], data["folder_ext2"]), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]), item))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".
                            format(data["folder_ext2"]), make_subfolder[0]))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}/{}".
                            format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
    assert all(res), "test6 FAIL"


def test_step7():
    # test7
    assert ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z d arx2.7z".
                        format(data["folder_out"]), "Everything is Ok"), "test7 FAIL"


def test_step8(clear_folders, make_files):
    # test8
    res = []
    for item in make_files:
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z h {}".
                                format(data["folder_in"], item), "Everything is Ok"))
        hash_data = ssh_getout(data["ip"], data["user"], data["passwd"], "cd {}; crc32 {}".
                               format(data["folder_in"], item)).upper()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z h {}".
                                format(data["folder_in"], item), hash_data))
    assert all(res), "test8 FAIL"
