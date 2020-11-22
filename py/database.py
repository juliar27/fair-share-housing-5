import os
from psycopg2 import connect
from googlemaps import Client as GoogleMaps
import py.parse

# ----------------------------------------------------------------------------------------------------------------------
def double_up(s):
    print(s)
    return s.replace("'", "''")
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def get_coordinates(address, county, map):
    fullAddress = address + ", " + county + ", " + "NJ, USA"
    coordinates = "error"

    try:
        geocode_result = map.geocode(fullAddress)
        latitude = geocode_result[0]['geometry']['location'] ['lat']
        longitude = geocode_result[0]['geometry']['location'] ['lng']
        coordinates = str(latitude) + "," + str(longitude)
    except:
        return(coordinates)

    return(coordinates)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
class Database:

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._connection = None

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        assert self
        self._connection = connect(host="ec2-52-21-247-176.compute-1.amazonaws.com",
                                   password="53f5293f5c753debb9340b4e662a0ba2c2f69a75ea5f18aa8dea9ca415a2df49",
                                   user="lxntyzuehczhml",
                                   port=5432,
                                   database="dcg0o6mcmqmeat")

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self):
        self._connection.commit()
        self._connection.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def clear(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM listings")
        cursor.execute("DELETE FROM addresses")
        cursor.execute("DELETE FROM cities")
        cursor.execute("DELETE FROM counties")

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def add_record(self, record, mapsObj):
        stmt = "INSERT INTO listings ("
        values = "VALUES ("
        pruned = record.copy()
        for column, value in record.items():
            if column in ('municipality', 'county', 'region', 'address'):
                if value == '':
                    del pruned[column]
                continue

            if column in ("compliance", 'name', 'developer', 'status', 'addresses', 'agent'):
                if value == '':
                    del pruned[column]
                    continue
                stmt += column + ", "
                values += "'" + double_up(value) + "', "
            else:
                stmt += column + ", "
                if value == '':
                    values += "0,"
                else:
                    values += value + ", "

        stmt = stmt[:-2] + ") "
        values = values[:-2] + ")"

        cursor = self._connection.cursor()
        cursor.execute(stmt + values)
        if "address" in pruned:
            # coordinates = "error"
            # if "county" in record:
            #     coordinates = get_coords(record["address"][0],record['county'], mapsObj)
            for address in record["address"]:
                stmt = "INSERT INTO addresses (listingid, address, coordinates) VALUES " \
                       + "('%s', '%s', '%s')" % (record["listingid"], double_up(address),"40.0,40.0")
                cursor.execute(stmt)
        if "municode" in pruned:
            stmt = "SELECT * FROM cities WHERE municode = " + record['municode']
            cursor.execute(stmt)

            if cursor.fetchone() is None:
                stmt = "INSERT INTO cities (municode, municipality, county)" \
                       + " VALUES (" + record['municode'] + ", '" + double_up(record['municipality']) + "', '" \
                       + double_up(record['county']) + "')"
                cursor.execute(stmt)

        if "county" in pruned and "region" in pruned:
            stmt = "SELECT * FROM counties WHERE county = '" + double_up(record['county']) + "'"
            cursor.execute(stmt)

            if cursor.fetchone() is None:
                stmt = "INSERT INTO counties (county, region)" \
                       + " VALUES ('" + double_up(record['county']) + "', " + record['region'] + ")"
                cursor.execute(stmt)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------
    def delete_record(self, listingid):
        cursor = self._connection.cursor()
        stmt = "DELETE FROM listings WHERE listingid = " + listingid
        cursor.execute(stmt)
        stmt = "DELETE FROM addresses WHERE listingid = " + listingid
        cursor.execute(stmt)
        cursor.close()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def edit_record(self, record, mapsObj):
        cursor = self._connection.cursor()
        if "addresses" in record:
            stmt = "SELECT addresses FROM listings WHERE listingid = " + record["listingid"]
            cursor.execute(stmt)
            row = cursor.fetchone()
            if row[0] == record['addresses']:
                del record['addresses']
                del record['address']

        stmt = "UPDATE listings SET "
        for column, value in record.items():
            if column in ('municipality', 'county', 'region', 'address'):
                continue
            stmt += column + " = "
            if column in ("compliance", 'name', 'developer', 'status', 'addresses', 'agent'):
                stmt += "'" + double_up(value) + "', "
            else:
                stmt += value + ", "
        stmt = stmt[:-2] + "WHERE listingid = " + record["listingid"]

        cursor.execute(stmt)
        if "address" in record:
            stmt = "DELETE FROM addresses WHERE listingid = " + record["listingid"]
            cursor.execute(stmt)

            for address in record["address"]:
                stmt = "INSERT INTO addresses (listingid, address, coordinates) VALUES " \
                       + "('%s', '%s','%s')" % (record["listingid"], double_up(address),"40.0,40.0")
                cursor.execute(stmt)
        cursor.close()

        return "address" in record
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_coords(self, changed_addresses):
        print(changed_addresses)
        mapsObj = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, cities.municipality, cities.county, addresses.address FROM listings, " + \
        "cities, addresses WHERE listings.municode = cities.municode AND listings.listingid = addresses.listingid"
        cursor.execute(stmt)
        row = cursor.fetchone()
        new_cursor = self._connection.cursor()

        while row is not None:
            print(row[0])
            if str(row[0]) in changed_addresses:
                print('getting')
                coordinates = get_coordinates(row[3], row[2], mapsObj)


                stmt = "UPDATE addresses SET coordinates = '" + coordinates + "' WHERE listingid = " + str(row[0])
                new_cursor.execute(stmt)

            row = cursor.fetchone()
        new_cursor.close()
        cursor.close()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def insert(self, record, mapsObj):
        cursor = self._connection.cursor()
        cursor.execute("SELECT 1 FROM listings WHERE listingid = " + record["listingid"])
        row = cursor.fetchone()

        if row is None:
            self.add_record(record, mapsObj)
            addressed = True
        else:
            addressed = self.edit_record(record, mapsObj)
        cursor.close()
        return addressed
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_rows(self):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, listings.name, listings.developer, listings.status, listings.compliance, listings.agent," + \
                "listings.addresses, cities.municipality, counties.county, cities.municode, counties.region, " + \
                "listings.v1, listings.v2, listings.v3, listings.l1, listings.l2, listings.l3, listings.m1, " + \
                "listings.m2, listings.m3, listings.vssn, listings.lssn, listings.mssn, listings.famsale, " + \
                "listings.famrent, listings.srsale, listings.srrent, listings.ssnsale, listings.ssnrent, " + \
                "listings.total, listings.family, listings.sr, listings.ssn, listings.br1, listings.br2, listings.br3 FROM " + \
               "listings, cities, counties WHERE " + \
               "listings.municode = cities.municode AND cities.county = counties.county ORDER BY listings.listingid"
        cursor.execute(stmt)
        rows = []
        row = cursor.fetchone()
        while row is not None:
            rows.append(row)
            row = cursor.fetchone()
        cursor.close()
        return rows
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_excel(self):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, cities.municode, cities.municipality, counties.county, counties.region, " + \
                "listings.name, listings.developer, listings.compliance, " + \
                "listings.addresses, listings.status, listings.agent, listings.total, listings.family, " + \
                "listings.famsale, listings.famrent, listings.sr, listings.srsale, listings.srrent, " + \
                "listings.ssnsale, listings.ssnrent, listings.br1, "  + \
                "listings.v1, listings.l1,  listings.m1, listings.br2, listings.v2, " + \
                "listings.l2, listings.m2, listings.br3, listings.v3, listings.l3," + \
                "listings.m3, listings.ssn, listings.vssn, listings.lssn, listings.mssn " + \
                "FROM " + \
               "listings, cities, counties WHERE " + \
               "listings.municode = cities.municode AND cities.county = counties.county ORDER BY listings.listingid"
        cursor.execute(stmt)
        rows = []
        row = cursor.fetchone()
        while row is not None:
            row = list(row)
            for i in range(11, len(row)):
                if row[i] is None:
                    row[i] = 0
            row.append(row[21] + row[25] + row[29])
            row.append(row[22] + row[26] + row[30])
            row.append(row[23] + row[27] + row[31])
            row.append(row[19] + row[17] + row[14])
            row.append(row[18] + row[16] + row[13])
            rows.append(row)
            row = cursor.fetchone()
        cursor.close()
        return rows
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def clear():
    database = Database()
    database.connect()
    database.clear()
    database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def delete(row):
    database = Database()
    database.connect()
    database.delete_record(row)
    database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def edit_listings(form):
    lookup = {0:'listingid', 1:'name', 2:'developer', 3:'status',
    4:'compliance', 5:'agent', 6:'address', 7:'municipality', 8:'county', 9:'municode',
    10:'region', 11:'v1', 12:'v2', 13:'v3', 14:'l1', 15:'l2',
    16:'l3', 17:'m1', 18:'m2', 19:'m3', 20:'vssn', 21:'lssn', 22:'mssn',
    23:'famsale', 24:'famrent', 25:'srsale', 26:'srrent', 27:'ssnsale',
    28:'ssnrent', 29:'total', 30:'family', 31:'sr', 32: 'ssn',
    33:'br1', 34:'br2', 35:'br3'}
    records = {}
    rows = get_tables()
    for item in form:
        current = item.split(';')
        value = form[item]
        if int(current[1]) > 9 and form[item] == 'None':
            value = '0'
        if int(current[0]) <= len(rows) and value == rows[int(current[0]) - 1][int(current[1])]:
            continue
        if not current[0] in records:
            records[current[0]] = {}
        records[current[0]][lookup[int(current[1])]] = value
    for record in records:
        edit_tables(records[record], record)

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def get_listings():
   database = Database()
   database.connect()
   cursor = database._connection.cursor()
   stmt = "SELECT listings.listingid, addresses.address, addresses.coordinates, cities.municipality, counties.county, listings.status, listings.br1," \
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
   result['id'] = listingid
   result['name'] = row[1]
   result['developer'] = row[2]
   result['status'] = row[3]
   result['compliance'] = row[4]
   result['municode'] = row[5]
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
   result['address'] = row[31]
   result['agent'] = row[32]
   result['muni'] = row[33]
   result['county'] = row[34]
   result['region'] = row[35]
   cursor.close()
   database.disconnect()
   return result
# ----------------------------------------------------------------------------------------------------------------------



def get_favorite_listings(favorites):
    database = Database()
    database.connect()
    ids = []
    rows = []
    for idadr in favorites:
        id = idadr.split(';')[0]
        adr = ';'.join(idadr.split(';')[1:])
        cursor = database._connection.cursor()
        stmt = "SELECT listings.listingid, addresses.address, addresses.coordinates, cities.municipality, counties.county, listings.status, listings.br1," \
          " listings.br2, listings.br3, listings.total, listings.family, listings.sr, listings.ssn FROM " + \
          "listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
          "listings.municode = cities.municode AND cities.county = counties.county AND listings.listingid = " + id + " AND addresses.address = '" + double_up(adr) + "'"
        cursor.execute(stmt)
        row = cursor.fetchone()

        ids.append(row[0])
        rows.append(row[1:])
    return rows, ids
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
   mapsObj = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')

   record = {'municode': form.get('municode'), 'municipality': form.get('muni'), 'county': form.get('county'),
             'region': form.get('region'), 'name': form.get('name'), 'developer': form.get('developer'),
             'compliance': form.get('compliance'), 'address': py.parse.parse_address(form.get('address')),
             'addresses': form.get('address'),
             'total': form.get('total'), 'family': form.get('family'), 'sr': form.get('senior'),
             'famsale': form.get('famsale'), 'famrent': form.get('famrent'), 'srsale': form.get('srsale'),
             'srrent': form.get('srrent'), 'ssn': form.get('ssn'), 'ssnsale': form.get('ssnsale'),
             'ssnrent': form.get('ssnrent'), 'v1': form.get('vli1'), 'v2': form.get('vli2'), 'v3': form.get('vli3'),
             'vssn': form.get('vssn'), 'l1': form.get('li1'), 'l2': form.get('li2'), 'l3': form.get('li3'),
             'lssn': form.get('lssn'), 'm1': form.get('m1'), 'm2': form.get('m2'), 'm3': form.get('m3'),
             'mssn': form.get('mssn'), 'br1': form.get('total1'), 'br2': form.get('total2'), 'br3': form.get('total3')}

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
   database.add_record(record, mapsObj)
   cursor.close()
   database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def edit_table(form, listingid):
   mapsObj = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')

   record = {'municode': form.get('municode'), 'municipality': form.get('muni'), 'county': form.get('county'),
             'region': form.get('region'), 'name': form.get('name'), 'developer': form.get('developer'),
             'compliance': form.get('compliance'), 'address': py.parse.parse_address(form.get('address')),
             'addresses': form.get('address'), 'agent': form.get('agent'),
             'total': form.get('total'), 'family': form.get('family'), 'sr': form.get('senior'),
             'famsale': form.get('famsale'), 'famrent': form.get('famrent'), 'srsale': form.get('srsale'),
             'srrent': form.get('srrent'), 'ssn': form.get('ssn'), 'ssnsale': form.get('ssnsale'),
             'ssnrent': form.get('ssnrent'), 'v1': form.get('vli1'), 'v2': form.get('vli2'), 'v3': form.get('vli3'),
             'vssn': form.get('vssn'), 'l1': form.get('li1'), 'l2': form.get('li2'), 'l3': form.get('li3'),
             'lssn': form.get('lssn'), 'm1': form.get('m1'), 'm2': form.get('m2'), 'm3': form.get('m3'),
             'mssn': form.get('mssn'), 'br1': form.get('total1'), 'br2': form.get('total2'), 'br3': form.get('total3')}

   # deletelist = []
   # for column, value in record.items():
   #     if value == '':
   #         deletelist.append(column)
   # for i in deletelist:
   #     del record[i]

   database = Database()
   database.connect()
   record['listingid'] = listingid
   database.edit_record(record, mapsObj)
   database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def edit_tables(record, listingid):
   mapsObj = None
   if 'address' in record:
       record['addresses'] = record['address']
       record['address'] = py.parse.parse_address(record['address'])

   record['listingid'] = listingid
   # deletelist = []
   # for column, value in record.items():
   #     if value == '':
   #         deletelist.append(column)
   # for i in deletelist:
   #     del record[i]

   database = Database()
   database.connect()
   database.insert(record, mapsObj)
   database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def coords():
    rows, ids = get_listings()
    x = []
    addressInfo = []
    for i in range(len(rows)):
        addr = str(rows[i][0])
        fullAddr = addr + ", " + str(rows[i][2]) + ", " + str(rows[i][3]) + " County, NJ USA"
        print(fullAddr)
        coords = rows[i][1].split(',')
        x.append([float(coords[0]), float(coords[1]), ids[i]])
        addressInfo.append([addr, rows[i][1], fullAddr])
    return x, addressInfo

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

def get_details(id, adr):
    db = Database()
    db.connect()

    stmt = "SELECT addresses.coordinates FROM addresses WHERE " + \
        "addresses.listingid = %s"

    cursor = db._connection.cursor()
    cursor.execute(stmt, [id])
    row = cursor.fetchone()

    if row is None:
        return 'Listing does not exist'

    return row

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def get_coords(changed_addresses):
   database = Database()
   database.connect()
   print("we doing")
   database.get_coords(changed_addresses)
   print("WE DIDDDDDDDDD")
   database.disconnect()
# ----------------------------------------------------------------------------------------------------------------------
