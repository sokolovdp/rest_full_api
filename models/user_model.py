# import sqlite3
from db_alchemy import db

# DB_NAME = 'app_data.db'
# find_user_by_name_query = "SELECT * FROM users WHERE username=?"
# find_user_by_id_query = "SELECT * FROM users WHERE id=?"


class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password_hash = db.Column(db.String(180))

    def __init__(self, user_name, password_hash):
        self.username = user_name
        self.password_hash = password_hash

    @classmethod
    def find_by_username(cls, user_name):
        return cls.query.filter_by(username=user_name).first()

        # connection = sqlite3.connect(DB_NAME)
        # cursor = connection.cursor()
        # result = cursor.execute(find_user_by_name_query, (user_name,))  # always tuple
        # row = result.fetchone()
        # connection.close()
        #
        # user = cls(*row) if row else None
        #
        # return user

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
        # connection = sqlite3.connect(DB_NAME)
        # cursor = connection.cursor()
        # result = cursor.execute(find_user_by_id_query, (user_id,))  # always tuple
        # row = result.fetchone()
        # connection.close()
        #
        # user = cls(*row) if row else None
        #
        # return user

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()
