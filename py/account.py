from py.database import Database
from py.auth import auth_email, recovery_email
from threading import Thread
import string
from queue import Queue
import random

# ----------------------------------------------------------------------------------------------------------------------
def account_get(userid):
    database = Database()
    database.connect()
    email = database.account_get(userid)
    database.disconnect()
    return email
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def make_account(user, server):
    try:
        database = Database()
        database.connect()
        is_new = database.start_account(user)
        if not is_new:
            return False
        id = database.get_id(email)[0]
        i = 0
        while i < 10:
            id += random.choice(string.ascii_letters)
            i += 1

        link = "fairsharehousing.herokuapp.com/authenticate?id=" + id
        auth_email(email, link, server)

        database.set_temp_where_email(id, email)
        database.disconnect()
        return True

    except:
        return False


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def check_account(user):

    try:
        email = user["inputEmailAddress"]
        password = user["inputPassword"]

        database = Database()
        database.connect()
        possible_password = database.get_password(email)
        if possible_password:
            encrypted_password = possible_password[0]
            ret = database.get_where_email_password(email, password, encrypted_password)
            if ret is None:
                database.disconnect()
                return False, False, False
            result = database.get_verified(email)[0]
            if not result:
                database.disconnect()
                return False, False, True
            id = database.get_id(email)
            return True, id[0], False
        database.disconnect()
        return False, False, False

    except:
        return False, False, False
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def authenticate(id):
    try:
        database = Database()
        database.connect()
        ret = database.authenticate(id)
        database.disconnect()
        return ret

    except:
        return False
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def valid_id(id):
    try:
        database = Database()
        database.connect()
        valid = database.valid_id(id)
        database.disconnect()
        return valid

    except:
        return False
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def update_password(dict):
    id = dict['id']
    password = dict['inputPassword']
    database = Database()
    database.connect()
    database.update_password(password, id)
    database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def recovery(dict, server):
    try:
        email = dict['inputEmailAddress']
        database = Database()
        database.connect()
        id = database.get_id(email)

        if id is not None:
            id = id[0]
        else:
            database.disconnect()
            return False, False

        if id is not None:
            verified = database.get_verified(email)[0]

            if verified:
                i = 0
                while i < 10:
                    id += random.choice(string.ascii_letters)
                    i += 1

                link = "fairsharehousing.herokuapp.com/recovery?id=" + id

                recovery_email(email, link,  server)

                database.set_temp_where_email(id, email)
                database.disconnect()

                return True, True

            else:
                database.disconnect()
                return True, False

        else:
            database.disconnect()
            return False, False

    except:
        return False, False
# ----------------------------------------------------------------------------------------------------------------------
