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
        errorMsg = "Error Inserting Row Number: " + str(row_number) + ". Please contact system administrator."

    else:
        errorMsg = "Incorrect Formatting at Column: " + col_name + " and Row Number: " + str(row_number)

    try:
        return url_for('show_parseerror', errorMsg=errorMsg)

    except Exception as e:
        print(argv[0] + ": " + str(e))

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def insert(sheet, database):

    d = {}
    row = sheet.row(0)
    for i in range(len(row)):
        d[row[i].value] = i

    i = 0
    row_number = 1

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
            return False, error('Municode', row_number)

        try:
            if row[d['Municipality']].ctype == XL_CELL_TEXT:
                record['municipality'] = row[d['Municipality']].value
        except:
            return  False, error('Municipality', row_number)

        try:
            if row[d['County']].ctype == XL_CELL_TEXT:
                record['county'] = row[d['County']].value
        except:
            return False, error('County', row_number)

        try:
            if row[d['Region']].ctype == XL_CELL_NUMBER:
                record['region'] = str(row[d['Region']].value)
        except:
            return False, error('Region', row_number)

        try:
            if row[d['SiteProgramName']].ctype == XL_CELL_TEXT:
                record['name'] = row[d['SiteProgramName']].value
        except:
            return False, error('SiteProgramName', row_number)

        try:
            if row[d['ProjectDeveloper']].ctype == XL_CELL_TEXT:
                record['developer'] = row[d['ProjectDeveloper']].value
        except:
            return False, error('ProjectDeveloper', row_number)

        try:
            if row[d['ComplianceMechanism']].ctype == XL_CELL_TEXT:
                record['compliance'] = row[d['ComplianceMechanism']].value
        except:
            return False, error('ComplianceMechanism', row_number)

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


        try:
            if row[d['Address']].ctype == XL_CELL_TEXT:
                if row[d['Address']].value not in ("TBD", "n/a", "N/A", "Site to be determined", "Various", "Varies- See Suppl Tab"):
                    record['address'] = parse_address(row[d['Address']].value)
                else:
                    return False, error('Address', row_number)
        except:
            return False, error('Address', row_number)

        try:
            if row[d['Status']].ctype == XL_CELL_TEXT:
                record['status'] = row[d['Status']].value
        except:
            return False, error('Status', row_number)

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

        try:
            if row[d['OverallTotalUnits']].ctype == XL_CELL_NUMBER:
                record['total'] = str(row[d['OverallTotalUnits']].value)
        except:
            return False, error('OverallTotalUnits', row_number)

        try:
            if row[d['TotalFamily']].ctype == XL_CELL_NUMBER:
                record['family'] = str(row[d['TotalFamily']].value)
        except:
            return False, error('TotalFamily', row_number)

        try:
            if row[d['FamilyForSale']].ctype == XL_CELL_NUMBER:
                record['famsale'] = str(row[d['FamilyForSale']].value)
        except:
            return False, error('FamilyForSale', row_number)

        try:
            if row[d['FamilyRental']].ctype == XL_CELL_NUMBER:
                record['famrent'] = str(row[d['FamilyRental']].value)
        except:
            return False, error('FamilyRental', row_number)


        try:
           if row[d['TotalAHProposed']].ctype == XL_CELL_NUMBER:
               record['proposed'] = str(row[d['TotalAHProposed']].value)
        except:
           error('TotalAHProposed', row_number)

        try:
           if row[d['TotalAHUnitsCompleted']].ctype == XL_CELL_NUMBER:
               record['completed'] = str(row[d['TotalAHUnitsCompleted']].value)
        except:
           error('TotalAHUnitsCompleted', row_number)

        try:
            if row[d['TotalSenior']].ctype == XL_CELL_NUMBER:
                record["sr"] = str(row[d['TotalSenior']].value)
        except:
            return False, error('TotalSenior', row_number)

        try:
            if row[d['SeniorForSale']].ctype == XL_CELL_NUMBER:
                record["srsale"] = str(row[d['SeniorForSale']].value)
        except:
            return False, error('SeniorForSale', row_number)

        try:
            if row[d['SeniorRental']].ctype == XL_CELL_NUMBER:
                record["srrent"] = str(row[d['SeniorRental']].value)
        except:
            return False, error('SeniorRental', row_number)

     #   try:
      #      if row[d['TotalSSN']].ctype == XL_CELL_NUMBER:
      #          record["total_ssn"] = str(row[d['TotalSSN']].value)
      #  except:
      #      error('TotalSSN', row_number)

        try:
            if row[d['SSNTotal']].ctype == XL_CELL_NUMBER:
                record["ssn"] = str(row[d['SSNTotal']].value)
        except:
            return False, error('SSNTotal', row_number)


        try:
            if row[d['SSNForSale']].ctype == XL_CELL_NUMBER:
                record["ssnsale"] = str(row[d['SSNForSale']].value)
        except:
            return False, error('SSNForSale', row_number)

        try:
            if row[d['SSNRental']].ctype == XL_CELL_NUMBER:
                record["ssnrent"] = str(row[d['SSNRental']].value)
        except:
            return False, error('SSNRental', row_number)

        try:
            if row[d['OneBRTotal']].ctype == XL_CELL_NUMBER:
                record["br1"] = str(row[d['OneBRTotal']].value)
        except:
            return False, error('OneBRTotal', row_number)

        try:
            if row[d['OneBRVLI']].ctype == XL_CELL_NUMBER:
                record["v1"] = str(row[d['OneBRVLI']].value)
        except:
            return False, error('OneBRVLI', row_number)

        try:
            if row[d['OneBRLow']].ctype == XL_CELL_NUMBER:
                record["l1"] = str(row[d['OneBRLow']].value)
        except:
            return False, error('OneBRLow', row_number)

        try:
            if row[d['OneBRMod']].ctype == XL_CELL_NUMBER:
                record["m1"] = str(row[d['OneBRMod']].value)
        except:
            return False, error('OneBRMod', row_number)

        try:
            if row[d['TwoBRTotal']].ctype == XL_CELL_NUMBER:
                record["br2"] = str(row[d['TwoBRTotal']].value)
        except:
            return False, error('TwoBRTotal', row_number)

        try:
            if row[d['TwoBRVLI']].ctype == XL_CELL_NUMBER:
                record["v2"] = str(row[d['TwoBRVLI']].value)
        except:
            return False, error('TwoBRVLI', row_number)

        try:
            if row[d['TwoBRLow']].ctype == XL_CELL_NUMBER:
                record["l2"] = str(row[d['TwoBRLow']].value)
        except:
            return False, error('TwoBRLow', row_number)

        try:
            if row[d['TwoBRMod']].ctype == XL_CELL_NUMBER:
                record["m2"] = str(row[d['TwoBRMod']].value)
        except:
            return False, error('TwoBRMod', row_number)

        try:
            if row[d['ThreeBRTotal']].ctype == XL_CELL_NUMBER:
                record["br3"] = str(row[d['ThreeBRTotal']].value)
        except:
            return False, error('ThreeBRTotal', row_number)

        try:
            if row[d['ThreeBRVLI']].ctype == XL_CELL_NUMBER:
                record["v3"] = str(row[d['ThreeBRVLI']].value)
        except:
            return False, error('ThreeBRVLI', row_number)

        try:
            if row[d['ThreeBRLow']].ctype == XL_CELL_NUMBER:
                record["l3"] = str(row[d['ThreeBRLow']].value)
        except:
            return False, error('ThreeBRLow', row_number)

        try:
            if row[d['ThreeBRMod']].ctype == XL_CELL_NUMBER:
                record["m3"] = str(row[d['ThreeBRMod']].value)
        except:
            return False, error('ThreeBRMod', row_number)


        try:
            if row[d['SSNBRVLI']].ctype == XL_CELL_NUMBER:
                record["vssn"] = str(row[d['SSNBRVLI']].value)
        except:
            return False, error('SSNBRVLI', row_number)

        try:
            if row[d['SSNBRLow']].ctype == XL_CELL_NUMBER:
                record["lssn"] = str(row[d['SSNBRLow']].value)
        except:
            return False, error('SSNBRLow', row_number)

        try:
            if row[d['SSNBRMod']].ctype == XL_CELL_NUMBER:
                record["mssn"] = str(row[d['SSNBRMod']].value)
        except:
            return False, error('SSNBRMod', row_number)

        if len(record) > 0:
            record["listingid"] = str(i)
            try:
                database.insert(record)
                i = i + 1
            except Exception as e:
                print(e)
                return False, error('Inserting', row_number)

        row_number += 1

    return True, "<br>Your records have been added to the database.</br>"

# ----------------------------------------------------------------------------------------------------------------------

    
# ----------------------------------------------------------------------------------------------------------------------
def parse_file(filename):
    wb = xlrd.open_workbook(file_contents=filename.read())
    sheet = wb.sheet_by_index(0)

    database = Database()
    database.connect()
    database.clear()

    html_status = insert(sheet, database)

    database.disconnect()
    return html_status
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
            end = int(s[index+1:])
        
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
