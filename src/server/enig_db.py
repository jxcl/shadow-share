import sqlite3
from datetime import datetime

class EnigDB():
    """Wrapper around shadowshare database."""
    def __init__(self, config):
        """Connect to the database."""
        self.conn = sqlite3.connect(config['DB_PATH'])
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def user_exists(self, user_name):
        """Check if the specified user exists in the database."""
        self.cursor.execute("select * from users where user_name=?",
                    (user_name,))

        result = self.cursor.fetchone()
        if (result == None):
            return False
        else:
            return (True, result)

    def register_user(self, user_name, key):
        """Add a user to the database with supplied public key."""
        self.cursor.execute("INSERT INTO users VALUES (?, ?)",
                            (user_name, key))
        self.conn.commit()

    def get_file_record(self, user_name):
        """Return file info of latest uploaded file of the specified user."""
        self.cursor.execute("SELECT * from files where user_name=?",
                            (user_name,))

        result = self.cursor.fetchone()
        return result

    def update_file_record(self, user_name, target_user, original_file_name):
        """Update the latest file info for specified user."""
        timestamp = datetime.strftime(datetime.now(),
                                      "%Y-%m-%dT%H:%M:%S")

        self.cursor.execute("""UPDATE files
                               SET target_user_name=?,
                               date_uploaded=?,
                               original_file_name=?
                               WHERE user_name=?""",
                            (target_user, timestamp,
                             user_name, original_file_name))
        self.conn.commit()

    def get_file_name(self, user_name):
        """Get the file name of the file stored by a specified user."""
        self.cursor.execute("SELECT * from files where user_name=?",
                            (user_name,))
        result = self.cursor.fetchone()['original_file_name']
        return result

    def create_file_record(self, user_name, target_user,
                           original_file_name):
        timestamp = datetime.strftime(datetime.now(),
                                      "%Y-%m-%dT%H:%M:%S")

        self.cursor.execute("INSERT INTO files VALUES (?, ?, ?, ?)",
                            (user_name, target_user,
                             original_file_name, timestamp))
        self.conn.commit()

    def close(self):
        """Close the connection."""
        self.conn.close()
