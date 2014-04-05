import sqlite3

class EnigDB():

    def __init__(self, config):
        self.rv = sqlite3.connect(config['DB_PATH'])
        self.rv.row_factory = sqlite3.Row
        self.cursor = self.rv.cursor()

    def user_exists(self, user_name):
        self.cursor.execute("select * from users where user_name=?",
                    (user_name,))
        if (self.cursor.fetchone() == None):
            return False
        else:
            return True

    def close(self):
        self.rv.close()
