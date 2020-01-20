from zinobe import TestZinobe


class UnitTestZinobe(object):
    test_zinobe = TestZinobe()

    def test_get_data_time(self):
        self.test_zinobe.get_data_time()

    def test_save_json_file(self):
        self.test_zinobe.save_json_file()

    def test_save_sqlite(self):
        self.test_zinobe.save_sqlite()
