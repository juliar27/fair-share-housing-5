import os
from psycopg2 import connect

class Database:
    def __init__(self):
        self._connection = None
    
    def connect(self):
        self._connection = connect(host="ec2-52-21-247-176.compute-1.amazonaws.com", password="53f5293f5c753debb9340b4e662a0ba2c2f69a75ea5f18aa8dea9ca415a2df49",
        user="lxntyzuehczhml", port=5432, database="dcg0o6mcmqmeat")

    def disconnect(self):
        self._connection.commit()
        self._connection.close()

    def add_record(self, record):
        stmt = "INSERT INTO listings ("
        values = "VALUES ("
        for column, value in record.items():
            if column == "address":
                continue
            stmt += column + ", "
            if column == "compliance":
                values += "'" + value + "', "
            else:
                values += value + ", "
        stmt = stmt[:-2] + ") "
        values = values[:-2] + ")"
        cursor = self._connection.cursor()
        cursor.execute(stmt + values)
        if "address" in record:
            for address in record["address"]:
                print(address)
                stmt = "INSERT INTO addresses (listingid, address) VALUES " \
                    + "('%s', '%s')" % (record["listingid"], address)
                cursor.execute(stmt)
        cursor.close()
    
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
    
    def insert(self, record):
        cursor = self._connection.cursor()
        cursor.execute("SELECT 1 FROM listings WHERE listingid = " + record["listingid"])
        row = cursor.fetchone()
        if row is None:
            self.add_record(record)
        else:
            self.edit_record(record)
        cursor.close()

