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

# ----------------------------------------------------------------------------------------------------------------------
def get_tables():
    database = Database()
    database.connect()
    rows = database.get_rows()
    database.disconnect()
    return rows


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def add_to_table(form):
    record = {'municode': form.get('municode'), 'municipality': form.get('municipality'), 'county': form.get('county'),
              'region': form.get('region'), 'name': form.get('name'), 'developer': form.get('developer'),
              'compliance': form.get('compliance'), 'address': parse_address(form.get('address')),
              'total': form.get('total'), 'family': form.get('family'), 'sr': form.get('senior'),
              'famsale': form.get('famsale'), 'famrent': form.get('famrent'), 'srsale': form.get('srsale'),
              'srrent': form.get('srrent'), 'ssn': form.get('ssn'), 'ssnsale': form.get('ssnsale'),
              'ssnrent': form.get('ssnrent'), 'v1': form.get('v1'), 'v2': form.get('v2'), 'v3': form.get('v3'),
              'vssn': form.get('vssn'), 'l1': form.get('l1'), 'l2': form.get('l2'), 'l3': form.get('l3'),
              'lssn': form.get('lssn'), 'm1': form.get('m1'), 'm2': form.get('m2'), 'm3': form.get('m3'),
              'mssn': form.get('mssn'), 'br1': form.get('br1'), 'br2': form.get('br2'), 'br3': form.get('br3')}

    deletelist = []
    for column, value in record.items():
        if value == '':
            deletelist.append(column)
    for i in deletelist:
        del record[i]

    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    cursor.execute('SELECT listingid from listings')
    row = cursor.fetchone()
    new_id = 1

    while row is not None:
        if int(row[0]) >= new_id:
            new_id = int(row[0]) + 1
        row = cursor.fetchone()
    record['listingid'] = str(new_id)
    database.add_record(record)
    cursor.close()
    database.disconnect()

    return
# ----------------------------------------------------------------------------------------------------------------------
