import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout_negative(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


folder_in = "/home/ream/tst"
folder_out = "/home/ream/out"
folder_ext = "/home/ream/folder1"


def test_step1():
    # test1
    res1 = checkout("cd {}; 7z a ../out/arx2".format(folder_in), "Everything is Ok")
    res2 = checkout("cd {}; 7z l arx2.7z".format(folder_out), "2 files")
    assert res1 and res2, "test1 FAIL"


def test_step2():
    # test2
    res1 = checkout("cd {}; 7z x arx2.7z -o/{} -y".format(folder_out, folder_ext), "Everything is Ok")
    assert res1, "test2 FAIL"


def test_nstep1():
    # neg test1 arx3.7z - break files
    res1 = checkout_negative("cd {}; 7z l arx3.7z".format(folder_out), "ERROR:")
    assert res1, "test1 FAIL"




