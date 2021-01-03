'''App Models'''
import datetime
from flask_login import UserMixin

from app.firestore_services import get_user

class UserData:
    def __init__(self, username, email, password,
                 admin=False, confirmed=False, confirmed_on=None):
        self.username = username
        self.email = email
        self.password = password
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on


class UserModel(UserMixin):
    def __init__(self, user_data):
        '''param user_data: UserData'''
        self.id = user_data.email
        self.username = user_data.username
        self.password = user_data.password
        self.confirmed = user_data.confirmed




    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            email=user_doc.id,
            username=user_doc.to_dict()['username'],
            password=user_doc.to_dict()['password']
        )
        return UserModel(user_data)
