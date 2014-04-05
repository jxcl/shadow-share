import sqlite3

class EnigDB():

    def __init__(self, config):
        self.rv = sqlite3.connect(config['DB_PATH'])
        self.rv.row_factory = sqlite3.Row
        self.cursor = self.rv.cursor()

    def user_exists(self, user_name):
        self.cursor.execute("select * from users where user_name=?",
                    (user_name,))

        result = self.cursor.fetchone()
        if (result == None):
            return False
        else:
            return (True, result)

    def register_user(self, user_name, key):
        self.cursor.execute("INSERT INTO users VALUES (?, ?)",
                            (user_name, key))

    def close(self):
        self.rv.close()
