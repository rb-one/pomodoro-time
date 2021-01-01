'''App Models'''

from flask_login import UserMixin

from app.firestore_services import get_user

class UserData:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class UserModel(UserMixin):
    def __init__(self, user_data):
        '''param user_data: UserData'''
        self.id = user_data.username
        self.email = user_data.email
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            email=user_doc.to_dict()['email'],
            password=user_doc.to_dict()['password']
        )
        return UserModel(user_data)
