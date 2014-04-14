import unittest
import tempfile
import server.shadowdb

class ShadowDBTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        config = {'DB_PATH': self.temp_file.name}

        self.db = server.shadowdb.ShadowDB(config)

    def test_nouser(self):
        self.assertFalse(self.db.user_exists("NonExistentUser"))

    def test_user_insert(self):
        self.db.register_user("hunter2", "falsekey")
        self.assertTrue(self.db.user_exists("hunter2"))

    def test_create_file_record(self):
        self.db.create_file_record("hunter2", "hunter2", "test.txt")

        expected_file_name = "test.txt"
        self.assertEquals(self.db.get_file_name("hunter2"), expected_file_name)

