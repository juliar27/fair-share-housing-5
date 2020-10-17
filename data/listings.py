from data.database import Database


# ----------------------------------------------------------------------------------------------------------------------
def get_listings():
    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    stmt = "SELECT addresses.address, cities.municipality, counties.county, listings.status, listings.br1," \
           " listings.br2, listings.br3, listings.total, listings.family, listings.sr, listings.ssn FROM " + \
           "listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
           "listings.municode = cities.municode AND cities.county = counties.county"
    cursor.execute(stmt)
    rows = []
    row = cursor.fetchone()
    while row is not None:
        rows.append(row)
        row = cursor.fetchone()

    database.disconnect()

    return rows
# ----------------------------------------------------------------------------------------------------------------------
