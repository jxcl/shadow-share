import unittest
import tempfile
import base64
from unittest import mock
import server.io


class IOTestCase(unittest.TestCase):

    def test_file_record_create(self):
        db = mock.Mock()
        db.get_file_record = mock.Mock(return_value="Something")
        db.update_file_record = mock.Mock()

        server.io.file_record(db, "hunter2", "tweed.txt")

        db.update_file_record.assert_called_once_with("hunter2",
                                                      None,
                                                      "tweed.txt")

    def test_file_record_update(self):
        db = mock.Mock()
        db.get_file_record = mock.Mock(return_value=None)
        db.create_file_record = mock.Mock()

        server.io.file_record(db, "hunter2", "tweed.txt")

        db.create_file_record.assert_called_once_with("hunter2",
                                                      None,
                                                      "tweed.txt")

    def test_open_and_encode(self):

        db = mock.Mock()
        db.get_file_name = mock.Mock(return_value="test.txt")

        temp_file = tempfile.NamedTemporaryFile(mode="w")
        temp_file.write("THIS IS A TEST")
        temp_file.seek(0)
        resp = server.io.open_and_encode_file(db, "hunter2",
                                              temp_file.name)


        expected_data = base64.b64encode(b'THIS IS A TEST').decode(
            'utf-8'
            )
        expected_response = {"status": "SUCCESS",
                             "file_name": "test.txt",
                             "data": expected_data
                             }
        self.assertEqual(resp, expected_response)


