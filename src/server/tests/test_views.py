import unittest
import json
import server.views
import server
import base64
import tempfile

test_key = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.12 (GNU/Linux)

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
5Fb1/YFp0g8pC5DKthpIM8bHiuA=
=OuRL
-----END PGP PUBLIC KEY BLOCK-----
'''

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        server.app.config['DB_URI'] = 'sqlite:///:memory:'
        server.app.config['UPLOAD_FOLDER'] = self.temp_dir.name
        server.init_engine(server.app)
        self.app = server.app.test_client()

    def test_nouser(self):
        r = self.app.get('/alex/retrieve/')
        r_json = json.loads(r.get_data().decode('utf-8'))

        self.assertEqual(r_json['status'], 'FAIL')
        self.assertEqual(r_json['error_message'], 'User does not exist.')

    def register_user_with_key(self, user_name, key):
        request_data = {'public_key': key}
        r = self.app.post('/{}/register/'.format(user_name),
                          data=json.dumps(request_data),
                          headers={'content-type': 'application/json'})
        r_json = json.loads(r.get_data().decode('utf-8'))
        return r_json

    def put_file(self, user_name, file_data, target_user=None):
        if target_user == None:
            target_user = user_name

        file_data_enc = base64.b64encode(bytearray(file_data, 'utf-8'))
        payload = {
            "file_name": "test.txt",
            "file_data": file_data_enc.decode('utf-8'),
            "file_target_user": target_user
            }

        r = self.app.post('/{}/store/'.format(user_name),
                          data=json.dumps(payload),
                          headers={'content-type': 'application/json'})
        return json.loads(r.get_data().decode('utf-8'))

    def get_file(self, user_name):
        r = self.app.get('/{}/retrieve/'.format(user_name))
        return json.loads(r.get_data().decode('utf-8'))

    def test_register_user(self):
        test_username = 'test-user'

        r_json = self.register_user_with_key(test_username, test_key)
        self.assertEquals(r_json['status'], 'SUCCESS')

    def test_register_user_badkey(self):
        test_user = 'test-user'
        r_json = self.register_user_with_key(test_user, "BOO!")
        self.assertEquals(r_json['error_message'],
                          "The provided key is not valid.")

    def test_double_register_user(self):
        test_username = 'test-user'

        r_json = self.register_user_with_key(test_username, test_key)
        self.assertEquals(r_json['status'], 'SUCCESS')

        r_json = self.register_user_with_key(test_username, test_key)
        self.assertEquals(r_json['status'], 'FAIL')

    def test_store(self):
        test_user = 'test-user'
        self.register_user_with_key(test_user, test_key)
        r = self.put_file(test_user, "HELLO THIS IS A TEST")
        self.assertEquals(r['status'], 'SUCCESS')

        r = self.get_file(test_user)
        self.assertEquals(r['status'], 'SUCCESS')

    def test_user_nofile(self):
        test_user = 'test-user'
        self.register_user_with_key(test_user, test_key)

        r = self.get_file(test_user)
        self.assertEquals(r['error_message'],
                          "User does not have a file stored.")

    def test_get_nouser(self):
        test_user = 'test-user'
        r = self.get_file(test_user)
        self.assertEquals(r['error_message'],
                          "User does not exist.")
    def test_getkey(self):
        test_user = 'test-user'
        self.register_user_with_key(test_user, test_key)
        r = self.app.get("/{}/get_key/".format(test_user))
        r_json = json.loads(r.get_data().decode('utf-8'))
        self.assertEquals(r_json['public_key'], test_key)


    def test_getkey_nouser(self):
        test_user = 'test-user'
        r = self.app.get("/{}/get_key/".format(test_user))
        r_json = json.loads(r.get_data().decode('utf-8'))
        self.assertEquals(r_json['error_message'], "No such user exists.")
