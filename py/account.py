from py.database import Database
from py.auth import auth_email, recovery_email
import string
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
def make_account(user):
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
            ret = True
        else:
            ret = False


        query = "SELECT id from users where email = %s ;;"
        cursor.execute(query, [email])
        id = cursor.fetchone()[0]

        i = 0
        while i < 10:
            id += random.choice(string.ascii_letters)
            i += 1

        query = "update users set temp_id = %s where email = %s ;;"

        cursor.execute(query, tuple([id, email]))
        database._connection.commit()
        database.disconnect()

        link = "fairsharehousing.herokuapp.com/authenticate?id=" + id
        auth_email(email, link)
        return ret
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
                ret = False, False, False
            else:
                query = "SELECT verified from users where email = %s ;;"
                cursor.execute(query, [email])
                result = cursor.fetchone()[0]
                if not result:
                    ret = False, False, True
                else:
                    query = "SELECT id from users where email = %s ;;"
                    cursor.execute(query, [email])
                    id = cursor.fetchone()

                    ret = True, id[0], False

        else:
            ret = False, False, False

        database.disconnect()
        return ret

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
        ret = False

        if cursor.fetchone() is not None:
            query = "update users set temp_id = NULL, verified = not verified where temp_id = %s ;;"
            cursor.execute(query, [id])
            database._connection.commit()
            ret = True

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
        cursor = database._connection.cursor()
        query = "select * from users where temp_id = %s ;;"
        cursor.execute(query, [id])
        ret = False

        if cursor.fetchone() is not None:
            ret = True

        database.disconnect()
        return ret

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
def recovery(dict):
    try:
        email = dict['inputEmailAddress']
        database = Database()
        database.connect()
        cursor = database._connection.cursor()
        query = "SELECT id from users where email = %s ;;"
        cursor.execute(query, [email])
        id = cursor.fetchone()
        ret = False, False

        if id is not None:
            id = id[0]


        if id is not None:
            query = "SELECT verified from users where email = %s ;;"
            cursor.execute(query, [email])
            verified = cursor.fetchone()[0]
            ret = True, False

            if verified:
                query = "SELECT temp_id from users where email = %s ;;"
                cursor.execute(query, [email])

                dup = cursor.fetchone()

                i = 0
                while i < 10:
                    id += random.choice(string.ascii_letters)
                    i += 1

                query = "update users set temp_id = %s where email = %s ;;"
                cursor.execute(query, tuple([id, email]))
                database._connection.commit()

                link = "fairsharehousing.herokuapp.com/recovery?id=" + id
                recovery_email(email, link)
                ret = True, True

        database.disconnect()
        return ret

    except:
        return False, False
# ----------------------------------------------------------------------------------------------------------------------
