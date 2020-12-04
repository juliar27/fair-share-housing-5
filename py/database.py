import os
from psycopg2 import connect
from googlemaps import Client as GoogleMaps

# ----------------------------------------------------------------------------------------------------------------------
def double_up(s):
    return s.replace("'", "''")
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def parse_hyphen(s, numbers):
    try:
        index = s.index('-', 1, -1)
        start, end = 0, 0
        if is_int(s[:index]):
            start = int(s[:index])
        if is_int(s[index + 1:]):
            end = int(s[index + 1:])

        if start > 0 and end > 0:
            numbers += [str(x) for x in range(start, end + 1)]
    except:
        if is_int(s) or s[-1].isalpha() and is_int(s[:-1]):
            numbers.append(s)


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def parse_comma(s):
    split = s.split(",")
    commas = len(split)
    split = [x.split() for x in split]
    split = [x for y in split for x in y]
    if split[commas - 1] == 'and':
        split.pop(commas - 1)
        commas += 1
    elif split[commas] == 'and':
        split.pop(commas)
        commas += 1
    numbers = []
    for i in range(commas):
        parse_hyphen(split[i], numbers)
    if len(numbers) == 0:
        return [s]
    streetname = ' '.join(split[commas:])
    return list(dict.fromkeys([x + " " + streetname for x in numbers]))

# ----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
def parse_address(s):
    if len(s) == 0:
        return []
    split = s.split(';')
    for i in range(len(split)):
        if split[i][0] in (' ', '\t', '\n'):
            split[i] = split[i][1:]
    split = sum([parse_comma(x) for x in split], [])
    return split
#-----------------------------------------------------------------------------------------------------------------------

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
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def add_record(self, record):
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
    def edit_record(self, record):
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
        mapsObj = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, cities.municipality, cities.county, addresses.address FROM listings, " + \
        "cities, addresses WHERE listings.municode = cities.municode AND listings.listingid = addresses.listingid"
        cursor.execute(stmt)
        row = cursor.fetchone()
        new_cursor = self._connection.cursor()

        while row is not None:
            if str(row[0]) in changed_addresses:
                coordinates = get_coordinates(row[3], row[2], mapsObj)


                stmt = "UPDATE addresses SET coordinates = '" + coordinates + "' WHERE listingid = " + str(row[0])
                new_cursor.execute(stmt)

            row = cursor.fetchone()
        new_cursor.close()
        cursor.close()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def insert(self, record):
        cursor = self._connection.cursor()
        cursor.execute("SELECT 1 FROM listings WHERE listingid = " + record["listingid"])
        row = cursor.fetchone()

        if row is None:
            self.add_record(record)
            addressed = True
        else:
            addressed = self.edit_record(record)
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
    def get_favorite_listings(self, ids, adrs):
        final_ids = []
        final_rows = []
        for i in range(len(ids)):
            id = ids[i]
            adr = adrs[i]
            cursor = self._connection.cursor()
            stmt = "SELECT listings.listingid, addresses.address, addresses.coordinates, cities.municipality, counties.county, listings.status, listings.br1," \
            " listings.br2, listings.br3, listings.total, listings.family, listings.sr, listings.ssn FROM " + \
            "listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
            "listings.municode = cities.municode AND cities.county = counties.county AND listings.listingid = " + id + " AND addresses.address = '" + double_up(adr) + "'"
            cursor.execute(stmt)
            row = cursor.fetchone()
            if row is not None and len(row) > 0:
                final_ids.append(row[0])
                final_rows.append(row[1:])
        cursor.close()
        return final_rows, final_ids
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_listings(self):
        cursor = self._connection.cursor()
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
        cursor.close()
        return rows, ids
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_location(self):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, addresses.address, addresses.coordinates, cities.municipality, counties.county," + \
                    "listings.status, listings.br1, listings.br2, listings.br3, listings.total, listings.v1, listings.v2, listings.v3, listings.l1, listings.l2," + \
                    "listings.l3, listings.m1, listings.m2, listings.m3, listings.vssn, listings.lssn, listings.mssn, listings.family, listings.sr," + \
                    "listings.total, listings.famsale, listings.famrent, listings.srsale, listings.srrent, listings.ssnsale, listings.ssnrent," + \
                    "listings.ssn FROM listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
                    "listings.municode = cities.municode AND cities.county = counties.county"
        cursor.execute(stmt)

        rows = []
        ids = []

        row = cursor.fetchone()
        while row is not None:
            ids.append(row[0])
            row = list(row)
            for i in range(6, 32):
                if row[i] is None:
                    row[i] = 0
            row = tuple(row)
            rows.append(row[1:])
            row = cursor.fetchone()
        cursor.close()

        return rows, ids
# ---------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_details(self, id, adr):
        stmt = "SELECT addresses.address, addresses.coordinates FROM addresses WHERE " + \
            "addresses.listingid = %s AND addresses.address = %s"

        cursor = self._connection.cursor()
        cursor.execute(stmt, (id, adr))
        row = cursor.fetchone()
        cursor.close()
        return row

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_row(self, listingid):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.*, cities.municipality, counties.county, counties.region FROM " + \
                "listings, cities, counties WHERE listings.listingid = " + str(listingid) + " AND " + \
                "listings.municode = cities.municode AND cities.county = counties.county"
        cursor.execute(stmt)
        row = list(cursor.fetchone())
        cursor.close()
        return row

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def account_get(self, userid):
        try:
            cursor = self._connection.cursor()
            query = "SELECT email from users where id = %s ;;"
            cursor.execute(query, [str(userid)])
            email = cursor.fetchone()
            cursor.close()
            if email is not None:
                return email[0]
            else:
                return None
        except:
            return None
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def start_account(self, user):
        first_name = user["inputFirstName"]
        last_name = user["inputLastName"]
        email = user["inputEmailAddress"]
        password = user["inputPassword"]

        cursor = self._connection.cursor()
        query = "SELECT * FROM users WHERE email = %s ;;"
        cursor.execute(query, [email])

        if cursor.fetchone() is None:
            query = "INSERT INTO users(email, password, first_name, last_name) VALUES(%s, crypt( %s, gen_salt('bf', 8)), %s, %s );"
            cursor.execute(query, tuple([email, password, first_name, last_name]))
            cursor.close()
            return True
        else:
            cursor.close()
            return False
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
    def get_password(self, email):
        cursor = self._connection.cursor()
        query = "SELECT password FROM users WHERE email = %s ;;"
        cursor.execute(query, [email])
        password = cursor.fetchone()
        cursor.close()
        return password
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_where_email_password(self, email, password, encrypted_password):
        cursor = self._connection.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = crypt(%s, %s);;"
        cursor.execute(query, tuple([email, password, encrypted_password]))
        ret = cursor.fetchone()
        cursor.close()
        return ret
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def authenticate(self, id):
        try:
            cursor = self._connection.cursor()
            query = "SELECT * FROM users WHERE temp_id = %s ;;"
            cursor.execute(query, [id])

            if cursor.fetchone() is not None:
                query = "UPDATE users SET temp_id = NULL, verified = NOT verified WHERE temp_id = %s ;;"
                cursor.execute(query, [id])
                cursor.close()
                return True
            cursor.close()
            return False
        except:
            return False
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def valid_id(self, id):
        try:
            cursor = self._connection.cursor()
            query = "SELECT * FROM users WHERE temp_id = %s ;;"
            cursor.execute(query, [id])
            ret = cursor.fetchone()
            cursor.close()
            return (ret is not None)
        except:
            return False
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def update_password(self, password, id):
        cursor = self._connection.cursor()
        query = "UPDATE users SET password = crypt(%s, gen_salt('md5')), temp_id = NULL WHERE temp_id = %s ;"
        cursor.execute(query, tuple([password, id]))
        cursor.close()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_id(self, email):
        cursor = self._connection.cursor()
        query = "SELECT id FROM users WHERE email = %s ;;"
        cursor.execute(query, [email])
        id = cursor.fetchone()
        cursor.close()
        return id
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def get_verified(self, email):
        cursor = self._connection.cursor()
        query = "SELECT verified FROM users WHERE email = %s ;;"
        cursor.execute(query, [email])
        verified = cursor.fetchone()
        cursor.close()
        return verified
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def set_temp_where_email(self, id, email):
        cursor = self._connection.cursor()
        query = "UPDATE users SET temp_id = %s WHERE email = %s ;;"
        cursor.execute(query, tuple([id, email]))
        cursor.close()
# ----------------------------------------------------------------------------------------------------------------------

