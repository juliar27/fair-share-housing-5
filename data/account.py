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

    query = "SELECT * from users where email = " + "'" + email + "'"

    cursor.execute(query)

    if cursor.fetchone() is None:
        ret = False
    else:
        query = "INSERT INTO users(email, password, first_name, last_name) VALUES(" + email + ", " + "crypt(" + \
                password + "'," + "gen_salt('bf'), " + first_name + ", " + last_name + ");"

        cursor.execute(query)
        ret = True

    database.disconnect()
    return ret
# ----------------------------------------------------------------------------------------------------------------------
