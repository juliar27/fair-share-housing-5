from py.database import Database

def get_details(id, adr):
    database = Database()
    database.connect()
    row = database.get_details(id, adr)
    database.disconnect()
    if row is None:
        return 'Listing does not exist'
    return row

def get_row(listingid):
    database = Database()
    database.connect()
    row = database.get_row(listingid)
    database.disconnect()

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

    return result