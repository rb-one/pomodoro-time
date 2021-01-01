import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users')\
            .document(user_id).get()


def get_pomodoros(user_id):
    return db.collection('users')\
            .document(user_id)\
            .collection('pomodoros').get()

def user_put(user_data):
    # creates a referece for document user_id
    user_ref = db.collection('users').document(user_data.username)
    # add email and password to the user referencedata
    # creates/set user in db
    user_ref.set({
        'email': user_data.email,
        'password': user_data.password
    })
