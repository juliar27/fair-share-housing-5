import os
from psycopg2 import connect


# ----------------------------------------------------------------------------------------------------------------------
def double_up(s):
    return s.replace("'", "''")


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
class Database:

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._connection = None

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
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
            if column == "br3":
                print(value)
                
            if column in ('municipality', 'county', 'region', 'address'):
                continue
            stmt += column + ", "
            if column in ("compliance", 'name', 'developer', 'status'):
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

        if "county" in record:
            stmt = "SELECT * FROM counties WHERE county = '" + double_up(record['county']) + "'"
            cursor.execute(stmt)

            if cursor.fetchone() is None:
                stmt = "INSERT INTO counties (county, region)" \
                       + " VALUES ('" + double_up(record['county']) + "', " + record['region'] + ")"
                cursor.execute(stmt)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def edit_record(self, record):
        stmt = "UPDATE listings SET "
        for column, value in record.items():
            if column == "address":
                continue
            stmt += column + " = "
            if column == "compliance":
                stmt += "'" + value + "', "
            else:
                stmt += value + ", "
        stmt = stmt[:-2] + "WHERE listingid = " + record["listingid"]
        cursor = self._connection.cursor()
        cursor.execute(stmt)
        if "address" in record:
            stmt = "DELETE FROM addresses WHERE listingid = " + record["listingid"]
            cursor.execute(stmt)
            for address in record["address"]:
                stmt = "INSERT INTO addresses (listingid, address) VALUES " \
                       + "('%s', '%s')" % (record["listingid"], address)
                cursor.execute(stmt)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def insert(self, record):
        # cursor = self._connection.cursor()
        # cursor.execute("SELECT 1 FROM listings WHERE listingid = " + record["listingid"])
        # row = cursor.fetchone()
        self.add_record(record)
        # if row is None:
        #     self.add_record(record)
        # else:
        #     self.edit_record(record)
        # cursor.close()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def get_rows(self):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.*, addresses.address, cities.municipality, counties.county, counties.region FROM " + \
               "listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
               "listings.municode = cities.municode AND cities.county = counties.county"
        cursor.execute(stmt)
        rows = []
        row = cursor.fetchone()
        while row is not None:
            rows.append(row)
            row = cursor.fetchone()
        cursor.close()
        return rows
    # ------------------------------------------------------------------------------------------------------------------

    def get_row(self, listingid):
        cursor = self._connection.cursor()
        stmt = "SELECT listings.*, cities.municipality, counties.county, counties.region FROM " + \
                "listings, cities, counties WHERE listings.listingid = " + str(listingid) + " AND " + \
                "listings.municode = cities.municode AND cities.county = counties.county"
        cursor.execute(stmt)
        row = cursor.fetchone()
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
        return result
# ----------------------------------------------------------------------------------------------------------------------
