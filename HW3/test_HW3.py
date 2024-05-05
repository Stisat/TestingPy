import yaml
from checkers import checkout, checkout_negative, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:


    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        res1 = checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        res2 = checkout("cd {}; ls".format(data["folder_out"]), "arx2.7z")
        assert res1 and res2, "test1 FAIL"


    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res), "test2 FAIL"


    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx2.7z".format(data["folder_out"]), "Everything is Ok"), "test3 FAIL"


    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u arx2.7z".format(data["folder_out"]), "Everything is Ok"), "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        # test1
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arx2.7z".format(data["folder_out"]), item))
        assert all(res), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout("cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.7z -o/{} -y".format(data["folder_out"], data["folder_ext2"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), item))
        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"


    def test_step7(self):
        # test7
        assert checkout("cd {}; 7z d arx2.7z".format(data["folder_out"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), hash))
        assert all(res), "test8 FAIL"


    def test_nstep1(self, clear_folders, damage_file):
        # negative test1
        assert checkout_negative("cd {}; 7z e arxbad.7z -o{}".format(data["folder_out"], data["folder_ext"]), "ERROR:"), "test_N1 FAIL"


    def test_nstep2(self, clear_folders, damage_file):
        # negative test2
        assert checkout_negative("cd {}; 7z t arxbad.7z".format(data["folder_out"]), "ERROR:"), "testN2 FAIL"

