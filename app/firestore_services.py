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
    user_ref = db.collection('users').document(user_data.email)
    # add email and password to the user referencedata
    # creates/set user in db
    user_ref.set({
        'username': user_data.username,
        'password': user_data.password,
        'registered_on': user_data.registered_on,
        'admin': user_data.admin,
        'confirmed': user_data.confirmed,
        'confirmed_on': user_data.confirmed_on
    })

def user_confirmed_update(user_data):
    user_ref = db.collection('users').document(user_data.email)
    user_ref.update({
        'confirmed': user_data.confirmed,
        'confirmed_on': user_data.confirmed_on
    })
