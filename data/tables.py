from data.database import Database
from data.parse import parse_address

# ----------------------------------------------------------------------------------------------------------------------
def get_listings():
    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    stmt = "SELECT listings.listingid, addresses.address, cities.municipality, counties.county, listings.status, listings.br1," \
           " listings.br2, listings.br3, listings.total, listings.family, listings.sr, listings.ssn FROM " + \
           "listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
           "listings.municode = cities.municode AND cities.county = counties.county"
    cursor.execute(stmt)
    rows = []
    ids = []
    row = cursor.fetchone()
    while row is not None:
        ids.append(row[0])
        rows.append(row[1:])
        row = cursor.fetchone()

    database.disconnect()

    return rows, ids
# ----------------------------------------------------------------------------------------------------------------------
 
def get_row(listingid):
    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    stmt = "SELECT listings.*, cities.municipality, counties.county, counties.region FROM " + \
            "listings, cities, counties WHERE listings.listingid = " + str(listingid) + " AND " + \
            "listings.municode = cities.municode AND cities.county = counties.county"
    cursor.execute(stmt)
    row = list(cursor.fetchone())
    for i in range(6, 31):
        if row[i] is None:
            row[i] = 0
    result = {}
    result['name'] = row[1]
    result['developer'] = row[2]
    result['status'] = row[3]
    result['compliance'] = row[4]
    result['vli1'] = row[6]
    result['vli2'] = row[7]
    result['vli3'] = row[8]
    result['li1'] = row[9]
    result['li2'] = row[10]
    result['li3'] = row[11]
    result['m1'] = row[12]
    result['m2'] = row[13] 
    result['m3'] = row[14]
    result['vssn'] = row[15]
    result['lssn'] = row[16]
    result['mssn'] = row[17]
    result['famsale'] = row[18]
    result['famrent'] = row[19]
    result['srsale'] = row[20]
    result['srrent'] = row[21]
    result['ssnsale'] = row[22]
    result['ssnrent'] = row[23]
    result['total'] = row[24]
    result['family'] = row[25]
    result['senior'] = row[26]
    result['ssn'] = row[27]
    result['total1'] = row[28]
    result['total2'] = row[29]
    result['total3'] = row[30]
    result['muni'] = row[31]
    result['county'] = row[32]
    cursor.close()
    database.disconnect()
    return result

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
