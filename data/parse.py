import xlrd
from data.database import Database
from sys import argv
from flask import redirect, url_for

# ----------------------------------------------------------------------------------------------------------------------
# a Unicode string
XL_CELL_TEXT = 1

# float
XL_CELL_NUMBER = 2

# date 
XL_CELL_DATE = 3


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def error(col_name, row_number):
    if col_name == 'Inserting':
        return "Error Inserting Row Number: " + str(row_number) + ". Please contact system administrator."

    elif col_name == 'Address':
        return "Row Number: " + str(row_number) + " must have an address."
    else:
        return "Incorrect Formatting at Column: " + col_name + " and Row Number: " + str(row_number) + ". "


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def get_listings(sheet, database):
    d = {}
    row = sheet.row(0)
    for i in range(len(row)):
        d[row[i].value] = i

    i = 0

    row_number = 1
    listing_id = 1

    listings = {}

    errors = []

    for row in sheet.get_rows():
        if i == 0:
            i += 1
            row_number += 1
            continue
        record = {}

        try:
            if row[d['Municode']].ctype == XL_CELL_NUMBER:
                record['municode'] = str(row[d['Municode']].value)
        except:
            errors.append(error('Municode', row_number))

        try:
            if row[d['Municipality']].ctype == XL_CELL_TEXT:
                record['municipality'] = row[d['Municipality']].value
        except:
            errors.append(error('Municipality', row_number))

        try:
            if row[d['County']].ctype == XL_CELL_TEXT:
                record['county'] = row[d['County']].value
        except:
            errors.append(error('County', row_number))

        try:
            if row[d['Region']].ctype == XL_CELL_NUMBER:
                record['region'] = str(row[d['Region']].value)
        except:
            errors.append(error('Region', row_number))

        try:
            if row[d['SiteProgramName']].ctype == XL_CELL_TEXT:
                record['name'] = row[d['SiteProgramName']].value
        except:
            errors.append(error('SiteProgramName', row_number))

        try:
            if row[d['ProjectDeveloper']].ctype == XL_CELL_TEXT:
                record['developer'] = row[d['ProjectDeveloper']].value
        except:
            errors.append(error('ProjectDeveloper', row_number))

        try:
            if row[d['ComplianceMechanism']].ctype == XL_CELL_TEXT:
                record['compliance'] = row[d['ComplianceMechanism']].value
        except:
            errors.append(error('ComplianceMechanism', row_number))


        try:
            if row[d['Address']].ctype == XL_CELL_TEXT:
                if row[d['Address']].value not in (
                "TBD", "n/a", "N/A", "Site to be determined", "Various", "Varies- See Suppl Tab"):
                    record['address'] = parse_address(row[d['Address']].value)
                    record['addresses'] = row[d['Address']].value
                else:
                    errors.append(error('Address', row_number))
        except:
            errors.append(error('Address', row_number))

        try:
            if row[d['Status']].ctype == XL_CELL_TEXT:
                record['status'] = row[d['Status']].value
        except:
            errors.append(error('Status', row_number))


        try:
            if row[d['OverallTotalUnits']].ctype == XL_CELL_NUMBER:
                record['total'] = str(row[d['OverallTotalUnits']].value)
        except:
            errors.append(error('OverallTotalUnits', row_number))

        try:
            if row[d['TotalFamily']].ctype == XL_CELL_NUMBER:
                record['family'] = str(row[d['TotalFamily']].value)
        except:
            errors.append(error('TotalFamily', row_number))

        try:
            if row[d['FamilyForSale']].ctype == XL_CELL_NUMBER:
                record['famsale'] = str(row[d['FamilyForSale']].value)
        except:
            errors.append(error('FamilyForSale', row_number))

        try:
            if row[d['FamilyRental']].ctype == XL_CELL_NUMBER:
                record['famrent'] = str(row[d['FamilyRental']].value)
        except:
            errors.append(error('FamilyRental', row_number))

        try:
            if row[d['TotalSenior']].ctype == XL_CELL_NUMBER:
                record["sr"] = str(row[d['TotalSenior']].value)
        except:
            errors.append(error('TotalSenior', row_number))

        try:
            if row[d['SeniorForSale']].ctype == XL_CELL_NUMBER:
                record["srsale"] = str(row[d['SeniorForSale']].value)
        except:
            errors.append(error('SeniorForSale', row_number))

        try:
            if row[d['SeniorRental']].ctype == XL_CELL_NUMBER:
                record["srrent"] = str(row[d['SeniorRental']].value)
        except:
            errors.append(error('SeniorRental', row_number))


        try:
            if row[d['SSNTotal']].ctype == XL_CELL_NUMBER:
                record["ssn"] = str(row[d['SSNTotal']].value)
        except:
            errors.append(error('SSNTotal', row_number))

        try:
            if row[d['SSNForSale']].ctype == XL_CELL_NUMBER:
                record["ssnsale"] = str(row[d['SSNForSale']].value)
        except:
            errors.append(error('SSNForSale', row_number))

        try:
            if row[d['SSNRental']].ctype == XL_CELL_NUMBER:
                record["ssnrent"] = str(row[d['SSNRental']].value)
        except:
            errors.append(error('SSNRental', row_number))

        try:
            if row[d['OneBRTotal']].ctype == XL_CELL_NUMBER:
                record["br1"] = str(row[d['OneBRTotal']].value)
        except:
            errors.append(error('OneBRTotal', row_number))

        try:
            if row[d['OneBRVLI']].ctype == XL_CELL_NUMBER:
                record["v1"] = str(row[d['OneBRVLI']].value)
        except:
            errors.append(error('OneBRVLI', row_number))

        try:
            if row[d['OneBRLow']].ctype == XL_CELL_NUMBER:
                record["l1"] = str(row[d['OneBRLow']].value)
        except:
            errors.append(error('OneBRLow', row_number))

        try:
            if row[d['OneBRMod']].ctype == XL_CELL_NUMBER:
                record["m1"] = str(row[d['OneBRMod']].value)
        except:
           errors.append(error('OneBRMod', row_number))

        try:
            if row[d['TwoBRTotal']].ctype == XL_CELL_NUMBER:
                record["br2"] = str(row[d['TwoBRTotal']].value)
        except:
            errors.append(error('TwoBRTotal', row_number))

        try:
            if row[d['TwoBRVLI']].ctype == XL_CELL_NUMBER:
                record["v2"] = str(row[d['TwoBRVLI']].value)
        except:
            errors.append(error('TwoBRVLI', row_number))

        try:
            if row[d['TwoBRLow']].ctype == XL_CELL_NUMBER:
                record["l2"] = str(row[d['TwoBRLow']].value)
        except:
            errors.append(error('TwoBRLow', row_number))

        try:
            if row[d['TwoBRMod']].ctype == XL_CELL_NUMBER:
                record["m2"] = str(row[d['TwoBRMod']].value)
        except:
            errors.append(error('TwoBRMod', row_number))

        try:
            if row[d['ThreeBRTotal']].ctype == XL_CELL_NUMBER:
                record["br3"] = str(row[d['ThreeBRTotal']].value)
        except:
            errors.append(error('ThreeBRTotal', row_number))

        try:
            if row[d['ThreeBRVLI']].ctype == XL_CELL_NUMBER:
                record["v3"] = str(row[d['ThreeBRVLI']].value)
        except:
            errors.append(error('ThreeBRVLI', row_number))

        try:
            if row[d['ThreeBRLow']].ctype == XL_CELL_NUMBER:
                record["l3"] = str(row[d['ThreeBRLow']].value)
        except:
            errors.append(error('ThreeBRLow', row_number))

        try:
            if row[d['ThreeBRMod']].ctype == XL_CELL_NUMBER:
                record["m3"] = str(row[d['ThreeBRMod']].value)
        except:
            errors.append(error('ThreeBRMod', row_number))

        try:
            if row[d['SSNBRVLI']].ctype == XL_CELL_NUMBER:
                record["vssn"] = str(row[d['SSNBRVLI']].value)
        except:
            errors.append(error('SSNBRVLI', row_number))

        try:
            if row[d['SSNBRLow']].ctype == XL_CELL_NUMBER:
                record["lssn"] = str(row[d['SSNBRLow']].value)
        except:
            errors.append(error('SSNBRLow', row_number))

        try:
            if row[d['SSNBRMod']].ctype == XL_CELL_NUMBER:
                record["mssn"] = str(row[d['SSNBRMod']].value)
        except:
            errors.append(error('SSNBRMod', row_number))

        if len(record) > 0:
            record["listingid"] = str(listing_id)

        row_number += 1
        listing_id += 1

        listings[listing_id] = record

    print(errors)
    return errors, listings


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def insert(database, records):

    errors = []

    for listings in records:
        try:
            database.insert(records[listings])
        except Exception as e:
            errors(error('Inserting', listings))

    return errors, records


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def parse_file(filename):
    wb = xlrd.open_workbook(file_contents=filename.read())
    sheet = wb.sheet_by_index(0)

    database = Database()
    database.connect()

    errors, listings = get_listings(sheet, database)

    if errors == []:
        database.clear()
        errors2, possible_redirect = insert(database, listings)

    else:
        database.disconnect()
        return False, url_for('show_parse_error', errorMsg=errors)

    database.disconnect()
    if errors2 == []:
        return True, possible_redirect
    else:
        return False, url_for('show_parse_error', errorMsg=errors2)
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


# ----------------------------------------------------------------------------------------------------------------------
def parse_address(s):
    if len(s) == 0:
        return []
    split = s.split(';')
    for i in range(len(split)):
        if split[i][0] in (' ', '\t', '\n'):
            split[i] = split[i][1:]
    split = sum([parse_comma(x) for x in split], [])
    return split
# ----------------------------------------------------------------------------------------------------------------------


# try:
#     if row[d['Round']].ctype == XL_CELL_NUMBER:
#         record['round'] = str(row[d['Round']].value)
# except:
#     return False, error('Round', row_number)

# try:
#     if row[d['Block']].ctype == XL_CELL_NUMBER:
#         record['block'] = str(row[d['Block']].value)
# except:
#     return False, error('Block', row_number)

# try:
#     if row[d['Lot']].ctype == XL_CELL_NUMBER:
#         record['lot'] = str(row[d['Lot']].value)
# except:
#     return False, error('Lot', row_number)
# try:
#     if row[d['DateBuildingPermitReceived']].ctype == XL_CELL_DATE:
#         record['permit'] = row[d['DateBuildingPermitReceived']].value
# except:
#     return False, error('DateBuildingPermitReceived', row_number)

# try:
#     if row[d['DateSitePlanSubdivision']].ctype == XL_CELL_DATE:
#         record['datesite'] = row[d['DateSitePlanSubdivision']].value
# except:
#     return False, error('DateSitePlanSubdivision', row_number)

# try:
#     if row[d['ExpectedCompletion']].ctype == XL_CELL_DATE:
#         record['ecompletion'] = row[d['ExpectedCompletion']].value
# except:
#     return False, error('ExpectedCompletion', row_number)

# try:
#     if row[d['DateControlsBegan']].ctype == XL_CELL_DATE:
#         record['dcbegan'] = row[d['DateControlsBegan']].value
# except:
#     return False, error('DateControlsBegan', row_number)

# try:
#     if row[d['LengthofControls']].ctype == XL_CELL_NUMBER:
#         record['locontrols'] = str(row[d['LengthofControls']].value)
# except:
#     return False, error('LengthofControls', row_number)

# try:
#     if row[d['AdminAgent']].ctype == XL_CELL_TEXT:
#         record['admin_agent'] = row[d['AdminAgent']].value
# except:
#     return False, error('AdminAgent', row_number)

# try:
#     if row[d['Contribution_PIL']].ctype == XL_CELL_NUMBER:
#         record['cpil'] = row[d['Contribution_PIL']].value
# except:
#     return False, error('Contribution_PIL', row_number)
#   try:
#      if row[d['TotalSSN']].ctype == XL_CELL_NUMBER:
#          record["total_ssn"] = str(row[d['TotalSSN']].value)
#  except:
#      error('TotalSSN', row_number)
