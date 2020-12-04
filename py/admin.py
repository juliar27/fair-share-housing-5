from py.database import Database, parse_address
from rq import Queue
from worker import conn
# ----------------------------------------------------------------------------------------------------------------------
def get_tables():
   database = Database()
   database.connect()
   rows = database.get_rows()
   database.disconnect()
   return rows
# ----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
def get_coords(changed_addresses):
   database = Database()
   database.connect()
   database.get_coords(changed_addresses)
   database.disconnect()
#-----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def edit_listings(form, q):
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

    database = Database()
    database.connect()
    changed_addresses = []
    for listingid in records:
        record = records[listingid]
        if 'address' in record:
            record['addresses'] = record['address']
            record['address'] = parse_address(record['address'])

        record['listingid'] = listingid
        changed = database.insert(record)
        if changed:
            changed_addresses.append(listingid)
    database.disconnect()

    q.enqueue(get_coords, changed_addresses)
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