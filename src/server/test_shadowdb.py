import unittest
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import server.shadowdb

class ShadowDBTestCase(unittest.TestCase):
    def setUp(self):
        engine = sqlalchemy.create_engine('sqlite:///:memory:')
        server.shadowdb.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.db = server.shadowdb.ShadowDB(self.session)

    def tearDown(self):
        self.session.close()

    def test_nouser(self):
        self.assertEquals(self.db.user_lookup("NonExistentUser"), None)

    def test_user_insert(self):
        self.db.register_user("hunter2", "falsekey")
        self.assertTrue(self.db.user_lookup("hunter2"))

    def test_create_file_record(self):
        self.db.create_file_record("hunter2", "hunter2", "test.txt")

        expected_file_name = "test.txt"
        self.assertEquals(self.db.get_file_name("hunter2"), expected_file_name)

    def test_update_file_record(self):
        first_expected = "test.txt"
        self.db.create_file_record("hunter2", "hunter2", first_expected)
        self.assertEquals(self.db.get_file_name("hunter2"),
                                                first_expected)

        second_expected = "test2.txt"
        self.db.update_file_record("hunter2", "leroy", second_expected)
        self.assertEquals(self.db.get_file_name("hunter2"),
                                                second_expected)


