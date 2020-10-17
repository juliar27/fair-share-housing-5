from data.database import Database


# ----------------------------------------------------------------------------------------------------------------------
def get_tables():
    database = Database()
    database.connect()
    rows = database.get_rows()
    database.disconnect()
    return rows

# ----------------------------------------------------------------------------------------------------------------------
