from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_name = Column(String, primary_key=True)
    public_key = Column(Text)

    def __repr__(self):
        return "<User (user_name='{}')>".format(self.user_name)

class FileRecord(Base):
    __tablename__ = 'files'

    user_name = Column(String, primary_key=True)
    target_user = Column(String)
    original_file_name = Column(String)
    timestamp = Column(String)

    def __repr__(self):
        return "<File (file_name='{}' user='{}')>".format(self.original_file_name,
                                                          self.user_name)

class ShadowDB():

    def __init__(self, session):
        self.session = session

    def user_lookup(self, user_name):
        return self.session.query(User).first()

    def register_user(self, user_name, pub_key):
        if self.user_lookup(user_name):
            raise ValueError("The specified user name already exists.")

        user = User(user_name=user_name, public_key=pub_key)
        self.session.add(user)
        self.session.commit()

    def get_file_name(self, user_name):
        query_result = self.session.query(FileRecord).filter_by(user_name=user_name)
        if query_result.count() == 0:
            return None
        else:
            name = query_result.first().original_file_name
            return name

    def create_file_record(self, user_name, target_user, file_name):

        timestamp = datetime.strftime(datetime.now(),
                                      "%Y-%m-%dT%H:%M:%S")
        f = FileRecord(user_name=user_name,
                       target_user=target_user,
                       original_file_name=file_name,
                       timestamp=timestamp)
        self.session.add(f)
        self.session.commit()

    def update_file_record(self, user_name, target_user, file_name):

        query_result = self.session.query(FileRecord).filter_by(user_name=user_name)
        record = query_result.first()
        record.target_user = target_user
        record.original_file_name = file_name

        self.session.commit()

    def get_file_record(self, user_name):
        return self.session.query(FileRecord).filter_by(user_name=user_name).first()
