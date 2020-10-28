from py.database import Database
from py.auth import auth

def account_get(userid):
    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    query = "SELECT email from users where id = " + "'" + str(userid) + "';;"
    cursor.execute(query)
    email = cursor.fetchone()
    database.disconnect()
    if email is not None:
        return email[0]
    else:
        return None

# ----------------------------------------------------------------------------------------------------------------------
def make_account(user):
    first_name = user["inputFirstName"]
    last_name = user["inputLastName"]
    email = user["inputEmailAddress"]
    password = user["inputPassword"]

    database = Database()
    database.connect()
    cursor = database._connection.cursor()

    query = "SELECT * from users where email = " + "'" + email + "';;"
    cursor.execute(query)

    if cursor.fetchone() is None:
        query = "INSERT INTO users(email, password, first_name, last_name) VALUES('" + email + "', " + "crypt('" + \
                password + "'," + "gen_salt('md5')), '" + first_name + "', '" + last_name + "');"
        cursor.execute(query)
        ret = True
    else:
        ret = False

    query = "SELECT id from users where email = " + "'" + email + "';;"
    cursor.execute(query)
    id = cursor.fetchone()
    database.disconnect()

    link = "fairsharehousing.herokuapp.com/authenticate?id=" + id[0]
# return redirect('/edit?id=' + request.args.get('id'))

    auth(email, link)


    return ret


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def check_account(user):

    email = user["inputEmailAddress"]
    password = user["inputPassword"]

    database = Database()
    database.connect()
    cursor = database._connection.cursor()

    query = "SELECT password from users where email = " + "'" + email + "' ;;"
    cursor.execute(query)

    possible_password = cursor.fetchone()

    if possible_password:
        encrypted_password = possible_password[0]

        query = "SELECT * from users where email = " + "'" + email + "' " + "and password = crypt('" +\
                password + "', '" + encrypted_password + "');;"
        cursor.execute(query)

        if cursor.fetchone() is None:
            ret = False, False
        else:
            query = "SELECT verified from users where email = " + "'" + email + "' ;;"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            if not result:
                ret = False, False
            else:
                query = "SELECT id from users where email = " + "'" + email + "' ;;"
                cursor.execute(query)
                id = cursor.fetchone()

                ret = True, id[0]

    else:
        ret = False, False

    database.disconnect()
    return ret
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def authenticate(id):
    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    query = "update users set verified = not verified where id = " + "'" + id + "'" +  ";;"
    cursor.execute(query)
    return ret

# ----------------------------------------------------------------------------------------------------------------------
