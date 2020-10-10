import xlrd
from data.database import Database
from PyQt5.QtWidgets import QApplication, QMainWindow
from sys import argv

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

    statement = "Incorrect Formatting at Column: " + col_name + "and Row Number: " + str(row_number)

    app = QApplication(argv)

    window = QMainWindow()
    window.setWindowTitle('Parsing Error')

    try:
        host = argv[1]
        port = int(argv[2])

        sock = socket()
        sock.connect((host, port))
        flo_rb = sock.makefile(mode='rb')

        QMessageBox.critical(window, statement, str(load(flo_rb)))
    except:
        print("ERROR")

# ----------------------------------------------------------------------------------------------------------------------

    
# ----------------------------------------------------------------------------------------------------------------------
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
    row_number = 0

    for row in sheet.get_rows():
        if i == 0:
            i = i + 1
            continue
        record = {}

        try:
            if row[d['Municode']].ctype == XL_CELL_NUMBER:
                record['municode'] = str(row[d['Municode']].value)
        except:
            error('Municode', row_number)

        try:
            if row[d['Municipality']].ctype == XL_CELL_TEXT:
                record['municipality'] = row[d['Municipality']].value
        except:
            error('Municipality', row_number)

        try:
            if row[d['County']].ctype == XL_CELL_TEXT:
                record['county'] = row[d['County']].value
        except:
            error('County', row_number)

        try:
            if row[d['Region']].ctype == XL_CELL_NUMBER:
                record['region'] = str(row[d['Region']].value)
        except:
            error('Region', row_number)

        try:
            if row[d['SiteProgramName']].ctype == XL_CELL_TEXT:
                record['name'] = row[d['SiteProgramName']].value
        except:
            error('SiteProgramName', row_number)

        try:
            if row[d['ProjectDeveloper']].ctype == XL_CELL_TEXT:
                record['developer'] = row[d['ProjectDeveloper']].value
        except:
            error('ProjectDeveloper', row_number)

        try:
            if row[d['ComplianceMechanism']].ctype == XL_CELL_TEXT:
                record['compliance'] = row[d['ComplianceMechanism']].value
        except:
            error('ComplianceMechanism', row_number)

        try:
            if row[d['Round']].ctype == XL_CELL_NUMBER:
                record['round'] = str(row[d['Round']].value)
        except:
            error('Round', row_number)

        try:
            if row[d['Block']].ctype == XL_CELL_NUMBER:
                record['block'] = str(row[d['Block']].value)
        except:
            error('Block', row_number)

        try:
            if row[d['Lot']].ctype == XL_CELL_NUMBER:
                record['lot'] = str(row[d['Lot']].value)
        except:
            error('Lot', row_number)


        try:
            if row[d['Address']].ctype == XL_CELL_TEXT:
                if row[d['Address']].value not in ("TBD", "n/a", "N/A", "Site to be determined", "Various", "Varies- See Suppl Tab"):
                    record['address'] = parse_address(row[d['Address']].value)
                else:
                    error('Address', row_number)
        except:
            error('Address', row_number)

        try:
            if row[d['Status']].ctype == XL_CELL_TEXT:
                record['status'] = row[d['Status']].value
        except:
            error('Status', row_number)

        try:
            if row[d['DateBuildingPermitReceived']].ctype == XL_CELL_DATE:
                record['permit'] = row[d['DateBuildingPermitReceived']].value
        except:
            error('DateBuildingPermitReceived', row_number)

        try:
            if row[d['DateSitePlanSubdivision']].ctype == XL_CELL_DATE:
                record['datesite'] = row[d['DateSitePlanSubdivision']].value
        except:
            error('DateSitePlanSubdivision', row_number)

        try:
            if row[d['ExpectedCompletion']].ctype == XL_CELL_DATE:
                record['ecompletion'] = row[d['ExpectedCompletion']].value
        except:
            error('ExpectedCompletion', row_number)

        try:
            if row[d['DateControlsBegan']].ctype == XL_CELL_DATE:
                record['dcbegan'] = row[d['DateControlsBegan']].value
        except:
            error('DateControlsBegan', row_number)

        try:
            if row[d['LengthofControls']].ctype == XL_CELL_NUMBER:
                record['locontrols'] = str(row[d['LengthofControls']].value)
        except:
            error('LengthofControls', row_number)

        try:
            if row[d['AdminAgent']].ctype == XL_CELL_TEXT:
                record['admin_agent'] = row[d['AdminAgent']].value
        except:
            error('AdminAgent', row_number)

        try:
            if row[d['Contribution_PIL']].ctype == XL_CELL_NUMBER:
                record['cpil'] = row[d['Contribution_PIL']].value
        except:
            error('Contribution_PIL', row_number)

        try:
            if row[d['OverallTotalUnits']].ctype == XL_CELL_NUMBER:
                record['tunits'] = row[d['OverallTotalUnits']].value
        except:
            error('OverallTotalUnits', row_number)

        try:
            if row[d['TotalFamily']].ctype == XL_CELL_NUMBER:
                record['tfamily'] = row[d['TotalFamily']].value
        except:
            error('TotalFamily', row_number)

        try:
            if row[d['FamilyForSale']].ctype == XL_CELL_NUMBER:
                record['ffsale'] = row[d['FamilyForSale']].value
        except:
            error('FamilyForSale', row_number)

        try:
            if row[d['FamilyRental']].ctype == XL_CELL_NUMBER:
                record['frental'] = row[d['FamilyRental']].value
        except:
            error('FamilyRental', row_number)


      # try:
      #      if row[d['TotalAHProposed']].ctype == XL_CELL_NUMBER:
      #          record['proposed'] = str(row[d['TotalAHProposed']].value)
      #  except:
      #      error('TotalAHProposed', row_number)

      #  try:
      #      if row[d['TotalAHUnitsCompleted']].ctype == XL_CELL_NUMBER:
      #          record['completed'] = str(row[d['TotalAHUnitsCompleted']].value)
      #  except:
      #      error('TotalAHUnitsCompleted', row_number)

        try:
            if row[d['TotalSenior']].ctype == XL_CELL_NUMBER:
                record["tsenior"] = str(row[d['TotalSenior']].value)
        except:
            error('TotalSenior', row_number)

        try:
            if row[d['SeniorForSale']].ctype == XL_CELL_NUMBER:
                record["srsale"] = str(row[d['SeniorForSale']].value)
        except:
            error('SeniorForSale', row_number)

        try:
            if row[d['SeniorRental']].ctype == XL_CELL_NUMBER:
                record["srrent"] = str(row[d['SeniorRental']].value)
        except:
            error('SeniorRental', row_number)

     #   try:
      #      if row[d['TotalSSN']].ctype == XL_CELL_NUMBER:
      #          record["total_ssn"] = str(row[d['TotalSSN']].value)
      #  except:
      #      error('TotalSSN', row_number)

        try:
            if row[d['SSNTotal']].ctype == XL_CELL_NUMBER:
                record["ssntotal"] = str(row[d['SSNTotal']].value)
        except:
            error('SSNTotal', row_number)


        try:
            if row[d['SSNForSale']].ctype == XL_CELL_NUMBER:
                record["ssnsale"] = str(row[d['SSNForSale']].value)
        except:
            error('SSNForSale', row_number)

        try:
            if row[d['SSNRental']].ctype == XL_CELL_NUMBER:
                record["ssnrent"] = str(row[d['SSNRental']].value)
        except:
            error('SSNRental', row_number)

        try:
            if row[d['OneBRTotal']].ctype == XL_CELL_NUMBER:
                record["obrtotal"] = str(row[d['OneBRTotal']].value)
        except:
            error('OneBRTotal', row_number)

        try:
            if row[d['OneBRVLI']].ctype == XL_CELL_NUMBER:
                record["v1"] = str(row[d['OneBRVLI']].value)
        except:
            error('OneBRVLI', row_number)

        try:
            if row[d['OneBRLow']].ctype == XL_CELL_NUMBER:
                record["l1"] = str(row[d['OneBRLow']].value)
        except:
            error('OneBRLow', row_number)

        try:
            if row[d['OneBRMod']].ctype == XL_CELL_NUMBER:
                record["m1"] = str(row[d['OneBRMod']].value)
        except:
            error('OneBRMod', row_number)

        try:
            if row[d['TwoBRTotal']].ctype == XL_CELL_NUMBER:
                record["tbrtotal"] = str(row[d['TwoBRTotal']].value)
        except:
            error('TwoBRTotal', row_number)

        try:
            if row[d['TwoBRVLI']].ctype == XL_CELL_NUMBER:
                record["v2"] = str(row[d['TwoBRVLI']].value)
        except:
            error('TwoBRVLI', row_number)

        try:
            if row[d['TwoBRLow']].ctype == XL_CELL_NUMBER:
                record["l2"] = str(row[d['TwoBRLow']].value)
        except:
            error('TwoBRLow', row_number)

        try:
            if row[d['TwoBRMod']].ctype == XL_CELL_NUMBER:
                record["m2"] = str(row[d['TwoBRMod']].value)
        except:
            error('TwoBRMod', row_number)

        try:
            if row[d['ThreeBRTotal']].ctype == XL_CELL_NUMBER:
                record["thbrtotal"] = str(row[d['ThreeBRTotal']].value)
        except:
            error('ThreeBRTotal', row_number)

        try:
            if row[d['ThreeBRVLI']].ctype == XL_CELL_NUMBER:
                record["v3"] = str(row[d['ThreeBRVLI']].value)
        except:
            error('ThreeBRVLI', row_number)

        try:
            if row[d['ThreeBRLow']].ctype == XL_CELL_NUMBER:
                record["l3"] = str(row[d['ThreeBRLow']].value)
        except:
            error('ThreeBRLow', row_number)

        try:
            if row[d['ThreeBRMod']].ctype == XL_CELL_NUMBER:
                record["m3"] = str(row[d['ThreeBRMod']].value)
        except:
            error('ThreeBRMod', row_number)


        try:
            if row[d['SSNBRVLI']].ctype == XL_CELL_NUMBER:
                record["vssn"] = str(row[d['SSNBRVLI']].value)
        except:
            error('SSNBRVLI', row_number)

        try:
            if row[d['SSNBRLow']].ctype == XL_CELL_NUMBER:
                record["lssn"] = str(row[d['SSNBRLow']].value)
        except:
            error('SSNBRLow', row_number)

        try:
            if row[d['SSNBRMod']].ctype == XL_CELL_NUMBER:
                record["mssn"] = str(row[d['SSNBRMod']].value)
        except:
            error('SSNBRMod', row_number)

        try:
            if row[d['Total Very Low Income Units']].ctype == XL_CELL_NUMBER:
                record["tvliu"] = str(row[d['Total Very Low Income Units']].value)
        except:
            error('Total Very Low Income Units', row_number)

        try:
            if row[d['Total Low-Income Units']].ctype == XL_CELL_NUMBER:
                record["tliu"] = str(row[d['Total Low-Income Units']].value)
        except:
            error('Total Low-Income Units', row_number)

        try:
            if row[d['Total Moderate-Income Units']].ctype == XL_CELL_NUMBER:
                record["tmiu"] = str(row[d['Total Moderate-Income Units']].value)
        except:
            error('Total Moderate-Income Units', row_number)

        try:
            if row[d['Rental']].ctype == XL_CELL_NUMBER:
                record["trental"] = str(row[d['Rental']].value)
        except:
            error('Rental', row_number)

        try:
            if row[d['For Sale']].ctype == XL_CELL_NUMBER:
                record["tsale"] = str(row[d['For Sale']].value)
        except:
            error('For Sale', row_number)

        if len(record) > 0:
            record["listingid"] = str(i)
            database.insert(record)
            i = i + 1

        row_number += 1


    database.disconnect()
    return "<br>Your records have been added to the database.</br>"
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
    split = s.split('; ')
    split = sum([parse_comma(x) for x in split], [])
    return split
# ----------------------------------------------------------------------------------------------------------------------
