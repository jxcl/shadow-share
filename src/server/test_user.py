import unittest
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from server.shadowdb import User, Base

class UserTestCase(unittest.TestCase):
    def setUp(self):
        engine = sqlalchemy.create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def test_no_users(self):
        result_count = self.session.query(User).count()
        self.assertEqual(0, result_count)

    def test_insert_user(self):
        test_user = User(user_name="test_user", public_key="KEEEEEEY")
        self.session.add(test_user)
        self.session.commit()

        query_result = self.session.query(User).all()[0]

        self.assertEqual(query_result.user_name, "test_user")


