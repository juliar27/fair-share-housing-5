from py.database import Database
from py.auth import auth_email, recovery_email
from threading import Thread
import string
from queue import Queue
import random

# ----------------------------------------------------------------------------------------------------------------------
def account_get(userid):
    try:
        database = Database()
        database.connect()
        cursor = database._connection.cursor()
        query = "SELECT email from users where id = %s ;;"
        cursor.execute(query, [str(userid)])
        email = cursor.fetchone()
        database.disconnect()
        if email is not None:
            return email[0]
        else:
            return None
    except:
        return None
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def make_account(user, server):
    try:
        first_name = user["inputFirstName"]
        last_name = user["inputLastName"]
        email = user["inputEmailAddress"]
        password = user["inputPassword"]

        database = Database()
        database.connect()
        cursor = database._connection.cursor()

        query = "SELECT * from users where email = %s ;;"
        cursor.execute(query, [email])

        if cursor.fetchone() is None:
            query = "INSERT INTO users(email, password, first_name, last_name) VALUES( %s, crypt( %s, gen_salt('bf', 8)),  %s, %s );"
            cursor.execute(query, tuple([email, password, first_name, last_name]))
        else:
            database.disconnect()
            return False

        query = "SELECT id from users where email = %s ;;"
        cursor.execute(query, [email])
        id = cursor.fetchone()[0]

        i = 0
        while i < 10:
            id += random.choice(string.ascii_letters)
            i += 1

        link = "fairsharehousing.herokuapp.com/authenticate?id=" + id
        auth_email(email, link, server)

        query = "update users set temp_id = %s where email = %s ;;"

        cursor.execute(query, tuple([id, email]))
        database._connection.commit()
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
        cursor = database._connection.cursor()

        query = "SELECT password from users where email = %s ;;"
        cursor.execute(query, [email])

        possible_password = cursor.fetchone()

        if possible_password:
            encrypted_password = possible_password[0]
            query = "SELECT * from users where email = %s and password = crypt(%s, %s);;"
            cursor.execute(query, tuple([email, password, encrypted_password]))

            if cursor.fetchone() is None:
                database.disconnect()
                return False, False, False

            else:
                query = "SELECT verified from users where email = %s ;;"
                cursor.execute(query, [email])
                result = cursor.fetchone()[0]
                if not result:
                    database.disconnect()
                    return False, False, True
                else:
                    query = "SELECT id from users where email = %s ;;"
                    cursor.execute(query, [email])
                    id = cursor.fetchone()
                    database.disconnect()
                    return True, id[0], False

        else:
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
        cursor = database._connection.cursor()
        query = "select * from users where temp_id = %s ;;"
        cursor.execute(query, [id])

        if cursor.fetchone() is not None:
            query = "update users set temp_id = NULL, verified = not verified where temp_id = %s ;;"
            cursor.execute(query, [id])
            database._connection.commit()
            database.disconnect()
            return True

        database.disconnect()
        return False

    except:
        return False
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def valid_id(id):
    try:
        database = Database()
        database.connect()
        cursor = database._connection.cursor()
        query = "select * from users where temp_id = %s ;;"
        cursor.execute(query, [id])

        if cursor.fetchone() is not None:
            database.disconnect()
            return True
        else:
            database.disconnect()
            return False

    except:
        return False
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def update_password(dict):
    try:
        id = dict['id']
        password = dict['inputPassword']
        database = Database()
        database.connect()
        cursor = database._connection.cursor()
        query = "update users set password = crypt(%s, gen_salt('md5')), temp_id = NULL where temp_id = %s ;"
        cursor.execute(query, tuple([password, id]))
        database._connection.commit()
        database.disconnect()
        return

    except:
        return
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def recovery(dict, server):
    try:
        email = dict['inputEmailAddress']
        database = Database()
        database.connect()
        cursor = database._connection.cursor()
        query = "SELECT id from users where email = %s ;;"
        cursor.execute(query, [email])
        id = cursor.fetchone()

        if id is not None:
            id = id[0]
        else:
            database.disconnect()
            return False, False

        if id is not None:
            query = "SELECT verified from users where email = %s ;;"
            cursor.execute(query, [email])
            verified = cursor.fetchone()[0]

            if verified:
                query = "SELECT temp_id from users where email = %s ;;"
                cursor.execute(query, [email])

                i = 0
                while i < 10:
                    id += random.choice(string.ascii_letters)
                    i += 1

                link = "fairsharehousing.herokuapp.com/recovery?id=" + id
                recovery_email(email, link,  server)

                query = "update users set temp_id = %s where email = %s ;;"
                cursor.execute(query, tuple([id, email]))
                database._connection.commit()
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
