import os
from psycopg2 import connect
from googlemaps import Client as GoogleMaps

# ----------------------------------------------------------------------------------------------------------------------
def double_up(s):
    return s.replace("'", "''")
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def get_coords(address, county):
    # mapsObj = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')
    # fullAddress = address + ", " + county + ", " + "NJ, USA"
    # coordinates = "error"
    # try:
    #     geocode_result = mapsObj.geocode(fullAddress)
    #     latitude = geocode_result[0]['geometry']['location'] ['lat']
    #     longitude = geocode_result[0]['geometry']['location'] ['lng']
    #     coordinates = str(latitude) + "," + str(longitude)
    # except:
    #     print("Address was wrong...")
    # return(coordinates)
    
    return "temp"
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
    def add_record(self, record):
        stmt = "INSERT INTO listings ("
        values = "VALUES ("

        for column, value in record.items():
            if column in ('municipality', 'county', 'region', 'address'):
                continue
            stmt += column + ", "
            if column in ("compliance", 'name', 'developer', 'status', 'addresses'):
                values += "'" + double_up(value) + "', "
            else:
                values += value + ", "

        stmt = stmt[:-2] + ") "
        values = values[:-2] + ")"

        cursor = self._connection.cursor()
        cursor.execute(stmt + values)
        if "address" in record:
            for address in record["address"]:
                stmt = "INSERT INTO addresses (listingid, address) VALUES " \
                       + "('%s', '%s')" % (record["listingid"], double_up(address))
                cursor.execute(stmt)
        if "municode" in record:
            stmt = "SELECT * FROM cities WHERE municode = " + record['municode']
            cursor.execute(stmt)

            if cursor.fetchone() is None:
                stmt = "INSERT INTO cities (municode, municipality, county)" \
                       + " VALUES (" + record['municode'] + ", '" + double_up(record['municipality']) + "', '" \
                       + double_up(record['county']) + "')"
                cursor.execute(stmt)

        if "county" in record and "region" in record:
            stmt = "SELECT * FROM counties WHERE county = '" + double_up(record['county']) + "'"
            cursor.execute(stmt)

            if cursor.fetchone() is None:
                stmt = "INSERT INTO counties (county, region)" \
                       + " VALUES ('" + double_up(record['county']) + "', " + record['region'] + ")"
                cursor.execute(stmt)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
    def delete_record(self, listingid):
        cursor = self._connection.cursor()
        stmt = "DELETE FROM listings WHERE listingid = " + listingid
        cursor.execute(stmt)
        stmt = "DELETE FROM addresses WHERE listingid = " + listingid
        cursor.execute(stmt)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
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
            if column in ("compliance", 'name', 'developer', 'status', 'addresses'):
                stmt += "'" + double_up(value) + "', "
            else:
                stmt += value + ", "
        stmt = stmt[:-2] + "WHERE listingid = " + record["listingid"]

        cursor.execute(stmt)
        if "address" in record:
            stmt = "DELETE FROM addresses WHERE listingid = " + record["listingid"]
            cursor.execute(stmt)
            for address in record["address"]:
                stmt = "INSERT INTO addresses (listingid, address) VALUES " \
                       + "('%s', '%s')" % (record["listingid"], double_up(address))
                cursor.execute(stmt)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def insert(self, record):
        cursor = self._connection.cursor()
        cursor.execute("SELECT 1 FROM listings WHERE listingid = " + record["listingid"])
        row = cursor.fetchone()

        if row is None:
            self.add_record(record)
        else:
            self.edit_record(record)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def get_rows(self):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, listings.name, listings.developer, listings.status, listings.compliance, " + \
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
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def get_excel(self):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.listingid, cities.municode, cities.municipality, counties.county, counties.region, " + \
                "listings.name, listings.developer, listings.compliance, " + \
                "listings.addresses, listings.status, listings.total, listings.family, " + \
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
            for i in range(10, len(row)):
                if row[i] is None:
                    row[i] = 0
            row.append(row[20] + row[24] + row[28])
            row.append(row[21] + row[25] + row[29])
            row.append(row[22] + row[26] + row[30])
            row.append(row[18] + row[16] + row[13])
            row.append(row[17] + row[15] + row[12])
            rows.append(row)
            row = cursor.fetchone()
        cursor.close()
        return rows
    # ------------------------------------------------------------------------------------------------------------------
   
# ----------------------------------------------------------------------------------------------------------------------
