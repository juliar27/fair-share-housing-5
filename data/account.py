from data.database import Database


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

    database.disconnect()
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
            ret = False
        else:
            ret = True

    else:
        ret = False

    database.disconnect()
    return ret
# ----------------------------------------------------------------------------------------------------------------------
