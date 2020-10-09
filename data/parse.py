import xlrd
from data.database import Database

def parse_file(filename):
    wb = xlrd.open_workbook(file_contents=filename.read())
    sheet = wb.sheet_by_index(0)

    d = {}
    row = sheet.row(0)
    for i in range(len(row)):
        d[row[i].value] = i 

    database = Database()
    database.connect()
    database.clear()
    i = 0
    for row in sheet.get_rows():
        if i == 0:
            i = i + 1
            continue
        record = {}

        if row[d['Municode']].ctype == 2:
            record['municode'] = str(row[d['Municode']].value)

        if row[d['Municipality']].ctype == 1:
            record['municipality'] = row[d['Municipality']].value

        if row[d['County']].ctype == 1:
            record['county'] = row[d['County']].value

        if row[d['Region']].ctype == 2:
            record['region'] = str(row[d['Region']].value)

        if row[d['SiteProgramName']].ctype == 1:
            record['name'] = row[d['SiteProgramName']].value

        if row[d['ProjectDeveloper']].ctype == 1:
            record['developer'] = row[d['ProjectDeveloper']].value

        if row[d['ComplianceMechanism']].ctype == 1:        
            record['compliance'] = row[d['ComplianceMechanism']].value

        if row[d['Address']].ctype == 1:
            if row[d['Address']].value not in ("TBD", "n/a", "N/A", "Site to be determined", "Various", "Varies- See Suppl Tab"):
                record['address'] = parse_address(row[d['Address']].value)
        
        if row[d['Status']].ctype == 1:
            record['status'] = row[d['Status']].value

        if row[d['TotalAHProposed']].ctype == 2:
            record['proposed'] = str(row[d['TotalAHProposed']].value)

        if row[d['TotalAHUnitsCompleted']].ctype == 2:
            record['completed'] = str(row[d['TotalAHUnitsCompleted']].value)
        
        if row[d['FamilyForSale']].ctype == 2:
            record["famsale"] = str(row[d['FamilyForSale']].value)

        if row[d['FamilyRental']].ctype == 2:
            record["famrent"] = str(row[d['FamilyRental']].value)

        if row[d['SeniorForSale']].ctype == 2:
            record["srsale"] = str(row[d['SeniorForSale']].value)
            
        if row[d['SeniorRental']].ctype == 2:
            record["srrent"] = str(row[d['SeniorRental']].value)

        if row[d['SSNForSale']].ctype == 2:
            record["ssnsale"] = str(row[d['SSNForSale']].value)

        if row[d['SSNRental']].ctype == 2:
            record["ssnrent"] = str(row[d['SSNRental']].value)

        if row[d['OneBRVLI']].ctype == 2:
            record["v1"] = str(row[d['OneBRVLI']].value)

        if row[d['OneBRLow']].ctype == 2:
            record["l1"] = str(row[d['OneBRLow']].value)

        if row[d['OneBRMod']].ctype == 2:
            record["m1"] = str(row[d['OneBRMod']].value)

        if row[d['TwoBRVLI']].ctype == 2:
            record["v2"] = str(row[d['TwoBRVLI']].value)

        if row[d['TwoBRLow']].ctype == 2:
            record["l2"] = str(row[d['TwoBRLow']].value)

        if row[d['TwoBRMod']].ctype == 2:
            record["m2"] = str(row[d['TwoBRMod']].value)

        if row[d['ThreeBRVLI']].ctype == 2:
            record["v3"] = str(row[d['ThreeBRVLI']].value)

        if row[d['ThreeBRLow']].ctype == 2:
            record["l3"] = str(row[d['ThreeBRLow']].value)

        if row[d['ThreeBRMod']].ctype == 2:
            record["m3"] = str(row[d['ThreeBRMod']].value) 

        if row[d['SSNBRVLI']].ctype == 2:
            record["vssn"] = str(row[d['SSNBRVLI']].value)

        if row[d['SSNBRLow']].ctype == 2:
            record["lssn"] = str(row[d['SSNBRLow']].value)

        if row[d['SSNBRMod']].ctype == 2:
            record["mssn"] = str(row[d['SSNBRMod']].value)
      
        if len(record) > 0:
            record["listingid"] = str(i)
            database.insert(record)
            i = i + 1
    database.disconnect()
    return "<br>Your records have been added to the database.</br>"

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False
    

def parse_hyphen(s, numbers):
    try:
        index = s.index('-', 1, -1)
        start, end = 0, 0
        if is_int(s[:index]):
            start = int(s[:index])
        if is_int(s[index + 1:]):
            end = int(s[index+1:])
        
        if start > 0 and end > 0:
            numbers += [str(x) for x in range(start, end + 1)]
    except:
        if is_int(s) or s[-1].isalpha() and is_int(s[:-1]):
            numbers.append(s)

def parse_comma(s):
    split = s.split(",")
    commas = len(split)
    split = [x.split() for x in split]
    split = [x for y in split for x in y]
    numbers = []
    for i in range(commas):
        parse_hyphen(split[i], numbers)
    if len(numbers) == 0:
        return [s]
    streetname = ' '.join(split[commas:])
    return list(dict.fromkeys([x + " " + streetname for x in numbers]))

def parse_address(s):
    if len(s) == 0:
        return []
    split = s.split('; ')
    split = sum([parse_comma(x) for x in split], [])
    return split
