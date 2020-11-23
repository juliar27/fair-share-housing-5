import xlrd
import py.database
from sys import argv
from flask import redirect, url_for
from googlemaps import Client as GoogleMaps

# ----------------------------------------------------------------------------------------------------------------------
# a Unicode string
XL_CELL_TEXT = 1

# float
XL_CELL_NUMBER = 2

# date
XL_CELL_DATE = 3


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def get_listings(sheet, database):
    d = {}

    expected = {'UNIQUEID': 'a Number',  'Municode': 'a Number', 'Municipality': 'Text',
    'County': 'Text', 'Region': 'a Number', 'SiteProgramName': 'Text', 'ProjectDeveloper': 'Text',
    'ComplianceMechanism': 'Text', 'AdminAgent': 'Text', 'Address': 'Text', 'Status': 'Text',
    'OverallTotalUnits': 'a Number', 'TotalFamily': 'a Number', 'FamilyForSale': 'a Number',
    'FamilyRental': 'a Number', 'TotalSenior': 'a Number', 'SeniorForSale': 'a Number', 'SeniorRental': 'a Number',
    'SSNTotal':  'a Number', 'SSNForSale': 'a Number', 'SSNRental': 'a Number', 'OneBRTotal': 'a Number',
    'OneBRVLI':  'a Number', 'OneBRLow': 'a Number', 'OneBRMod': 'a Number', 'TwoBRTotal': 'a Number',
    'TwoBRVLI': 'a Number', 'TwoBRLow': 'a Number',  'TwoBRMod': 'a Number', 'ThreeBRTotal': 'a Number',
    'ThreeBRVLI': 'a Number', 'ThreeBRLow':  'a Number',  'ThreeBRMod': 'a Number',
     'SSNBRVLI': 'a Number', 'SSNBRLow':  'a Number', 'SSNBRMod':  'a Number'}


    if sheet.nrows > 0:
        row = sheet.row(0)
    else:
        missing_columns = ['UNIQUEID', 'Municode', 'Municipality', 'County'
        , 'Region','SiteProgramName', 'ProjectDeveloper', 'ComplianceMechanism',
        'AdminAgent', 'Address', 'Status', 'OverallTotalUnits', 'TotalFamily',
        'FamilyForSale', 'FamilyRental', 'TotalSenior', 'SeniorForSale',
        'SeniorRental', 'SSNTotal', 'SSNForSale', 'SSNRental', 'OneBRTotal',
        'OneBRVLI', 'OneBRLow', 'OneBRMod', 'TwoBRTotal', 'TwoBRVLI', 'TwoBRLow',
        'TwoBRMod', 'ThreeBRTotal', 'ThreeBRVLI', 'ThreeBRLow', 'ThreeBRMod',
        'SSNBRVLI', 'SSNBRLow', 'SSNBRMod']

        missing_columns_type = []

        for i  in missing_columns:
            missing_columns_type.append(expected[i])

        return True, missing_columns, missing_columns_type, [], [], []

    for i in range(len(row)):
        d[row[i].value] = i

    i = 0

    row_number = 1

    listings = {}

    rand = {}
    missing_columns = []

    for row in sheet.get_rows():
        if i == 0:
            i += 1
            row_number += 1
            continue
        record = {}

        try:
            if row[d['UNIQUEID']].ctype == XL_CELL_NUMBER:
                record['listingid'] = str(int(row[d['UNIQUEID']].value))
            elif row[d['UNIQUEID']].value.strip() == "":
                pass
            else:
                if 'UNIQUEID' not in rand:
                    rand['UNIQUEID'] = str(row_number)
                else:
                    rand['UNIQUEID'] = rand['UNIQUEID'] + ", " + str(row_number)

        except:
            if 'UNIQUEID' not in missing_columns:
                missing_columns.append('UNIQUEID')

        try:
            if row[d['Municode']].ctype == XL_CELL_NUMBER:
                record['municode'] = str(row[d['Municode']].value)

            elif row[d['Municode']].value.strip() == "":
                pass

            else:
                if 'Municode' not in rand:
                    rand['Municode'] = str(row_number)
                else:
                    rand['Municode'] = rand['Municode'] + ", " + str(row_number)

        except:
            if 'Municode' not in missing_columns:
                missing_columns.append('Municode')

        try:
            if row[d['Municipality']].ctype == XL_CELL_TEXT:
                record['municipality'] = row[d['Municipality']].value

            elif row[d['Municipality']].value.strip() == "":
                pass

            else:
                if 'Municipality' not in rand:
                    rand['Municipality'] = str(row_number)
                else:
                    rand['Municipality'] = rand['Municipality'] + ", " + str(row_number)


        except:
            if 'Municipality' not in missing_columns:
                missing_columns.append('Municipality')

        try:
            if row[d['County']].ctype == XL_CELL_TEXT:
                record['county'] = row[d['County']].value

            elif row[d['County']].value.strip() == "":
                pass

            else:
                if 'County' not in rand:
                    rand['County'] = str(row_number)
                else:
                    rand['County'] = rand['County'] + ", " + str(row_number)

        except:
            if 'County' not in missing_columns:
                missing_columns.append('County')

        try:
            if row[d['Region']].ctype == XL_CELL_NUMBER:
                record['region'] = str(row[d['Region']].value)

            elif row[d['Region']].value.strip() == "":
                pass

            else:
                if 'Region' not in rand:
                    rand['Region'] = str(row_number)
                else:
                    rand['Region'] = rand['Region'] + ", " + str(row_number)


        except:
            if 'Region' not in missing_columns:
                missing_columns.append('Region')

        try:
            if row[d['SiteProgramName']].ctype == XL_CELL_TEXT:
                record['name'] = row[d['SiteProgramName']].value

            elif row[d['SiteProgramName']].value.strip() == "":
                pass

            else:
                if 'SiteProgramName' not in rand:
                    rand['SiteProgramName'] = str(row_number)
                else:
                    rand['SiteProgramName'] = rand['SiteProgramName'] + ", " + str(row_number)

        except:
            if 'SiteProgramName' not in missing_columns:
                missing_columns.append('SiteProgramName')

        try:
            if row[d['ProjectDeveloper']].ctype == XL_CELL_TEXT:
                record['developer'] = row[d['ProjectDeveloper']].value

            elif row[d['ProjectDeveloper']].value.strip() == "":
                pass

            else:
                if 'ProjectDeveloper' not in rand:
                    rand['ProjectDeveloper'] = str(row_number)
                else:
                    rand['ProjectDeveloper'] = rand['ProjectDeveloper'] + ", " + str(row_number)


        except:
            if 'ProjectDeveloper' not in missing_columns:
                missing_columns.append('ProjectDeveloper')

        try:
            if row[d['ComplianceMechanism']].ctype == XL_CELL_TEXT:
                record['compliance'] = row[d['ComplianceMechanism']].value

            elif row[d['ComplianceMechanism']].value.strip() == "":
                pass

            else:
                if 'ComplianceMechanism' not in rand:
                    rand['ComplianceMechanism'] = str(row_number)
                else:
                    rand['ComplianceMechanism'] = rand['ComplianceMechanism'] + ", " + str(row_number)



        except:
            if 'ComplianceMechanism' not in missing_columns:
                missing_columns.append('ComplianceMechanism')

        try:
            if row[d['AdminAgent']].ctype == XL_CELL_TEXT:
                record['agent'] = row[d['AdminAgent']].value

            elif row[d['AdminAgent']].value.strip() == "":
                pass

            else:
                if 'AdminAgent' not in rand:
                    rand['AdminAgent'] = str(row_number)
                else:
                    rand['AdminAgent'] = rand['AdminAgent'] + ", " + str(row_number)

        except:
            if 'AdminAgent' not in missing_columns:
                missing_columns.append('AdminAgent')

        try:
            if row[d['Address']].ctype == XL_CELL_TEXT:
                if row[d['Address']].value not in \
                        ("TBD", "n/a", "", "N/A", "Site to be determined", "Various", "Varies- See Suppl Tab"):
                    record['address'] = parse_address(row[d['Address']].value)
                    record['addresses'] = row[d['Address']].value

                else:
                    if 'Address' not in rand:
                        rand['Address'] = str(row_number)
                    else:
                        rand['Address'] = rand['Address'] + ", " + str(row_number)



            elif row[d['Address']].value.strip() == "":
                pass

            else:
                if 'Address' not in rand:
                    rand['Address'] = str(row_number)
                else:
                    rand['Address'] = rand['Address'] + ", " + str(row_number)


        except:
            if 'Address' not in missing_columns:
                missing_columns.append('Address')

        try:
            if row[d['Status']].ctype == XL_CELL_TEXT:
                record['status'] = row[d['Status']].value

            elif row[d['Status']].value.strip() == "":
                pass

            else:
                if 'Status' not in rand:
                    rand['Status'] = str(row_number)
                else:
                    rand['Status'] = rand['Status'] + ", " + str(row_number)



        except:
            if 'Status' not in missing_columns:
                missing_columns.append('Status')

        try:
            if row[d['OverallTotalUnits']].ctype == XL_CELL_NUMBER:
                record['total'] = str(row[d['OverallTotalUnits']].value)

            elif row[d['OverallTotalUnits']].value.strip() == "":
                pass

            else:
                if 'OverallTotalUnits' not in rand:
                    rand['OverallTotalUnits'] = str(row_number)
                else:
                    rand['OverallTotalUnits'] = rand['OverallTotalUnits'] + ", " + str(row_number)



        except:
            if 'OverallTotalUnits' not in missing_columns:
                missing_columns.append('OverallTotalUnits')

        try:
            if row[d['TotalFamily']].ctype == XL_CELL_NUMBER:
                record['family'] = str(row[d['TotalFamily']].value)

            elif row[d['TotalFamily']].value.strip() == "":
                pass

            else:
                if 'TotalFamily' not in rand:
                    rand['TotalFamily'] = str(row_number)
                else:
                    rand['TotalFamily'] = rand['TotalFamily'] + ", " + str(row_number)




        except:
            if 'TotalFamily' not in missing_columns:
                missing_columns.append('TotalFamily')

        try:
            if row[d['FamilyForSale']].ctype == XL_CELL_NUMBER:
                record['famsale'] = str(row[d['FamilyForSale']].value)

            elif row[d['FamilyForSale']].value.strip() == "":
                pass

            else:
                if 'FamilyForSale' not in rand:
                    rand['FamilyForSale'] = str(row_number)
                else:
                    rand['FamilyForSale'] = rand['FamilyForSale'] + ", " + str(row_number)


        except:
            if 'FamilyForSale' not in missing_columns:
                missing_columns.append('FamilyForSale')

        try:
            if row[d['FamilyRental']].ctype == XL_CELL_NUMBER:
                record['famrent'] = str(row[d['FamilyRental']].value)

            elif row[d['FamilyRental']].value.strip() == "":
                pass

            else:
                if 'FamilyRental' not in rand:
                    rand['FamilyRental'] = str(row_number)
                else:
                    rand['FamilyRental'] = rand['FamilyRental'] + ", " + str(row_number)


        except:
            if 'FamilyRental' not in missing_columns:
                missing_columns.append('FamilyRental')

        try:
            if row[d['TotalSenior']].ctype == XL_CELL_NUMBER:
                record["sr"] = str(row[d['TotalSenior']].value)

            elif row[d['TotalSenior']].value.strip() == "":
                pass

            else:
                if 'TotalSenior' not in rand:
                    rand['TotalSenior'] = str(row_number)
                else:
                    rand['TotalSenior'] = rand['TotalSenior'] + ", " + str(row_number)



        except:
            if 'TotalSenior' not in missing_columns:
                missing_columns.append('TotalSenior')

        try:
            if row[d['SeniorForSale']].ctype == XL_CELL_NUMBER:
                record["srsale"] = str(row[d['SeniorForSale']].value)

            elif row[d['SeniorForSale']].value.strip() == "":
                pass

            else:
                if 'SeniorForSale' not in rand:
                    rand['SeniorForSale'] = str(row_number)
                else:
                    rand['SeniorForSale'] = rand['SeniorForSale'] + ", " + str(row_number)


        except:
            if 'SeniorForSale' not in missing_columns:
                missing_columns.append('SeniorForSale')

        try:
            if row[d['SeniorRental']].ctype == XL_CELL_NUMBER:
                record["srrent"] = str(row[d['SeniorRental']].value)

            elif row[d['SeniorRental']].value.strip() == "":
                pass

            else:
                if 'SeniorRental' not in rand:
                    rand['SeniorRental'] = str(row_number)
                else:
                    rand['SeniorRental'] = rand['SeniorRental'] + ", " + str(row_number)


        except:
            if 'SeniorRental' not in missing_columns:
                missing_columns.append('SeniorRental')

        try:
            if row[d['SSNTotal']].ctype == XL_CELL_NUMBER:
                record["ssn"] = str(row[d['SSNTotal']].value)

            elif row[d['SSNTotal']].value.strip() == "":
                pass

            else:
                if 'SSNTotal' not in rand:
                    rand['SSNTotal'] = str(row_number)
                else:
                    rand['SSNTotal'] = rand['SSNTotal'] + ", " + str(row_number)


        except:
            if 'SSNTotal' not in missing_columns:
                missing_columns.append('SSNTotal')

        try:
            if row[d['SSNForSale']].ctype == XL_CELL_NUMBER:
                record["ssnsale"] = str(row[d['SSNForSale']].value)

            elif row[d['SSNForSale']].value.strip() == "":
                pass

            else:
                if 'SSNForSale' not in rand:
                    rand['SSNForSale'] = str(row_number)
                else:
                    rand['SSNForSale'] = rand['SSNForSale'] + ", " + str(row_number)


        except:
            if 'SSNForSale' not in missing_columns:
                missing_columns.append('SSNForSale')

        try:
            if row[d['SSNRental']].ctype == XL_CELL_NUMBER:
                record["ssnrent"] = str(row[d['SSNRental']].value)

            elif row[d['SSNRental']].value.strip() == "":
                pass

            else:
                if 'SSNRental' not in rand:
                    rand['SSNRental'] = str(row_number)
                else:
                    rand['SSNRental'] = rand['SSNRental'] + ", " + str(row_number)


        except:
            if 'SSNRental' not in missing_columns:
                missing_columns.append('SSNRental')

        try:
            if row[d['OneBRTotal']].ctype == XL_CELL_NUMBER:
                record["br1"] = str(row[d['OneBRTotal']].value)

            elif row[d['OneBRTotal']].value.strip() == "":
                pass

            else:
                if 'OneBRTotal' not in rand:
                    rand['OneBRTotal'] = str(row_number)
                else:
                    rand['OneBRTotal'] = rand['OneBRTotal'] + ", " + str(row_number)


        except:
            if 'OneBRTotal' not in missing_columns:
                missing_columns.append('OneBRTotal')

        try:
            if row[d['OneBRVLI']].ctype == XL_CELL_NUMBER:
                record["v1"] = str(row[d['OneBRVLI']].value)

            elif row[d['OneBRVLI']].value.strip() == "":
                pass

            else:
                if 'OneBRVLI' not in rand:
                    rand['OneBRVLI'] = str(row_number)
                else:
                    rand['OneBRVLI'] = rand['OneBRVLI'] + ", " + str(row_number)


        except:
            if 'OneBRVLI' not in missing_columns:
                missing_columns.append('OneBRVLI')

        try:
            if row[d['OneBRLow']].ctype == XL_CELL_NUMBER:
                record["l1"] = str(row[d['OneBRLow']].value)

            elif row[d['OneBRLow']].value.strip() == "":
                pass

            else:
                if 'OneBRLow' not in rand:
                    rand['OneBRLow'] = str(row_number)
                else:
                    rand['OneBRLow'] = rand['OneBRLow'] + ", " + str(row_number)



        except:
            if 'OneBRLow' not in missing_columns:
                missing_columns.append('OneBRLow')

        try:
            if row[d['OneBRMod']].ctype == XL_CELL_NUMBER:
                record["m1"] = str(row[d['OneBRMod']].value)

            elif row[d['OneBRMod']].value.strip() == "":
                pass

            else:
                if 'OneBRMod' not in rand:
                    rand['OneBRMod'] = str(row_number)
                else:
                    rand['OneBRMod'] = rand['OneBRMod'] + ", " + str(row_number)


        except:
            if 'OneBRMod' not in missing_columns:
                missing_columns.append('OneBRMod')

        try:
            if row[d['TwoBRTotal']].ctype == XL_CELL_NUMBER:
                record["br2"] = str(row[d['TwoBRTotal']].value)

            elif row[d['TwoBRTotal']].value.strip() == "":
                pass

            else:
                if 'TwoBRTotal' not in rand:
                    rand['TwoBRTotal'] = str(row_number)
                else:
                    rand['TwoBRTotal'] = rand['TwoBRTotal'] + ", " + str(row_number)


        except:
            if 'TwoBRTotal' not in missing_columns:
                missing_columns.append('TwoBRTotal')

        try:
            if row[d['TwoBRVLI']].ctype == XL_CELL_NUMBER:
                record["v2"] = str(row[d['TwoBRVLI']].value)

            elif row[d['TwoBRVLI']].value.strip() == "":
                pass

            else:
                if 'TwoBRVLI' not in rand:
                    rand['TwoBRVLI'] = str(row_number)
                else:
                    rand['TwoBRVLI'] = rand['TwoBRVLI'] + ", " + str(row_number)


        except:
            if 'TwoBRVLI' not in missing_columns:
                missing_columns.append('TwoBRVLI')

        try:
            if row[d['TwoBRLow']].ctype == XL_CELL_NUMBER:
                record["l2"] = str(row[d['TwoBRLow']].value)

            elif row[d['TwoBRLow']].value.strip() == "":
                pass

            else:
                if 'TwoBRLow' not in rand:
                    rand['TwoBRLow'] = str(row_number)
                else:
                    rand['TwoBRLow'] = rand['TwoBRLow'] + ", " + str(row_number)


        except:
            if 'TwoBRLow' not in missing_columns:
                missing_columns.append('TwoBRLow')

        try:
            if row[d['TwoBRMod']].ctype == XL_CELL_NUMBER:
                record["m2"] = str(row[d['TwoBRMod']].value)

            elif row[d['TwoBRMod']].value.strip() == "":
                pass

            else:
                if 'TwoBRMod' not in rand:
                    rand['TwoBRMod'] = str(row_number)
                else:
                    rand['TwoBRMod'] = rand['TwoBRMod'] + ", " + str(row_number)



        except:
            if 'TwoBRMod' not in missing_columns:
                missing_columns.append('TwoBRMod')

        try:
            if row[d['ThreeBRTotal']].ctype == XL_CELL_NUMBER:
                record["br3"] = str(row[d['ThreeBRTotal']].value)

            elif row[d['ThreeBRTotal']].value.strip() == "":
                pass

            else:
                if 'ThreeBRTotal' not in rand:
                    rand['ThreeBRTotal'] = str(row_number)
                else:
                    rand['ThreeBRTotal'] = rand['ThreeBRTotal'] + ", " + str(row_number)


        except:
            if 'ThreeBRTotal' not in missing_columns:
                missing_columns.append('ThreeBRTotal')

        try:
            if row[d['ThreeBRVLI']].ctype == XL_CELL_NUMBER:
                record["v3"] = str(row[d['ThreeBRVLI']].value)

            elif row[d['ThreeBRVLI']].value.strip() == "":
                pass

            else:
                if 'ThreeBRVLI' not in rand:
                    rand['ThreeBRVLI'] = str(row_number)
                else:
                    rand['ThreeBRVLI'] = rand['ThreeBRVLI'] + ", " + str(row_number)


        except:
            if 'ThreeBRVLI' not in missing_columns:
                missing_columns.append('ThreeBRVLI')

        try:
            if row[d['ThreeBRLow']].ctype == XL_CELL_NUMBER:
                record["l3"] = str(row[d['ThreeBRLow']].value)

            elif row[d['ThreeBRLow']].value.strip() == "":
                pass

            else:
                if 'ThreeBRLow' not in rand:
                    rand['ThreeBRLow'] = str(row_number)
                else:
                    rand['ThreeBRLow'] = rand['ThreeBRLow'] + ", " + str(row_number)



        except:
            if 'ThreeBRLow' not in missing_columns:
                missing_columns.append('ThreeBRLow')

        try:
            if row[d['ThreeBRMod']].ctype == XL_CELL_NUMBER:
                record["m3"] = str(row[d['ThreeBRMod']].value)

            elif row[d['ThreeBRMod']].value.strip() == "":
                pass

            else:
                if 'ThreeBRMod' not in rand:
                    rand['ThreeBRMod'] = str(row_number)
                else:
                    rand['ThreeBRMod'] = rand['ThreeBRMod'] + ", " + str(row_number)


        except:
            if 'ThreeBRMod' not in missing_columns:
                missing_columns.append('ThreeBRMod')

        try:
            if row[d['SSNBRVLI']].ctype == XL_CELL_NUMBER:
                record["vssn"] = str(row[d['SSNBRVLI']].value)

            elif row[d['SSNBRVLI']].value.strip() == "":
                pass

            else:
                if 'SSNBRVLI' not in rand:
                    rand['SSNBRVLI'] = str(row_number)
                else:
                    rand['SSNBRVLI'] = rand['SSNBRVLI'] + ", " + str(row_number)


        except:
            if 'SSNBRVLI' not in missing_columns:
                missing_columns.append('SSNBRVLI')

        try:
            if row[d['SSNBRLow']].ctype == XL_CELL_NUMBER:
                record["lssn"] = str(row[d['SSNBRLow']].value)

            elif row[d['SSNBRLow']].value.strip() == "":
                pass

            else:
                if 'SSNBRLow' not in rand:
                    rand['SSNBRLow'] = str(row_number)
                else:
                    rand['SSNBRLow'] = rand['SSNBRLow'] + ", " + str(row_number)


        except:
            if 'SSNBRLow' not in missing_columns:
                missing_columns.append('SSNBRLow')

        try:
            if row[d['SSNBRMod']].ctype == XL_CELL_NUMBER:
                record["mssn"] = str(row[d['SSNBRMod']].value)

            elif row[d['SSNBRMod']].value.strip() == "":
                pass

            else:
                if 'SSNBRMod' not in rand:
                    rand['SSNBRMod'] = str(row_number)
                else:
                    rand['SSNBRMod'] = rand['SSNBRMod'] + ", " + str(row_number)


        except:
            if 'SSNBRMod' not in missing_columns:
                missing_columns.append('SSNBRMod')

        row_number += 1

        listings[row_number] = record

    missing_columns_type = []
    for i in missing_columns:
        missing_columns_type.append(expected[i])

    wrongtype = []
    wrongtype_expected = []

    for i in rand:
        num = " "
        num += rand[i]
        wrongtype.append(i + ": " + num)
        wrongtype_expected.append(expected[i])

    return False, missing_columns, missing_columns_type, wrongtype, wrongtype_expected, listings


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def insert(database, records):
    mapsObj = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')

    changed_addresses = []
    for listings in records:
        try:
            changed_addr = database.insert(records[listings], mapsObj)
            if changed_addr:
                changed_addresses.append(records[listings]['listingid'])
        except Exception as e:
            print(str(e))

    return records, changed_addresses


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def parse_file(filename):
    wb = xlrd.open_workbook(file_contents=filename.read())
    sheet = wb.sheet_by_index(0)

    database = py.database.Database()
    database.connect()

    empty_flag, missing_columns, missing_columns_type, wrongtype, wrongtype_expected, listings = get_listings(sheet, database)

    if empty_flag:
        return False, url_for('show_parse_error', missing_columns=missing_columns, missing_columns_type=missing_columns_type, wrongtype=[],  wrongtype_expected=[]), False

    if missing_columns == [] and wrongtype == []:
         records, changed_addresses = insert(database, listings)
    else:
        database.disconnect()
        return False, url_for('show_parse_error', missing_columns=missing_columns, missing_columns_type=missing_columns_type, wrongtype=wrongtype,  wrongtype_expected=wrongtype_expected), False

    database.disconnect()
    return True, records, changed_addresses
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
