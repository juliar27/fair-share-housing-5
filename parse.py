import xlrd
#from database import Database
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('admin.html')

#@app.route('/upload', methods = ['GET', 'POST'])
# def parse_file():
#     if request.method == 'GET':
#         return

#     filename = request.files['sheet']
#     wb = xlrd.open_workbook(filename)
#     sheet = wb.sheet_by_index(2)

#     database = Database()
#     database.connect()
#     addresses = []
#     record = {}
#     i = 0
#     for row in sheet.get_rows():
#         if i == 0:
#             i = i + 1
#             continue
#         if row[0].ctype == 0 and row[11].ctype == 1:
#             addresses.append(row[11].value)
#         else:
#             if len(record) > 0:
#                 record["address"] = sum([parse_addresses(x) for x in addresses], [])
#                 addresses = []
#                 if i == 0:
#                     i = i + 1
#                     record = {}
#                     continue
#                 record["listingid"] = str(i)
#                 database.insert(record)
#                 record = {}
#                 i = i + 1
#             if row[1].ctype == 2:
#                 record["municode"] = str(row[1].value)
#             if row[6].ctype == 1:
#                 record["compliance"] = row[6].value
#             if row[11].ctype == 1:
#                 addresses.append(row[11].value)
#             if row[22].ctype == 2:
#                 record["proposed"] = str(row[22].value)
#             if row[23].ctype == 2:
#                 record["completed"] = str(row[23].value)
#             if row[25].ctype == 2:
#                 record["famsale"] = str(row[25].value)
#             if row[26].ctype == 2:
#                 record["famrent"] = str(row[26].value)
#             if row[28].ctype == 2:
#                 record["srsale"] = str(row[28].value)
#             if row[29].ctype == 2:
#                 record["srrent"] = str(row[29].value)
#             if row[31].ctype == 2:
#                 record["ssnsale"] = str(row[31].value)
#             if row[32].ctype == 2:
#                 record["ssnrent"] = str(row[32].value)
#             if row[34].ctype == 2:
#                 record["v1"] = str(row[34].value)
#             if row[35].ctype == 2:
#                 record["l1"] = str(row[35].value)
#             if row[36].ctype == 2:
#                 record["m1"] = str(row[36].value)
#             if row[38].ctype == 2:
#                 record["v2"] = str(row[38].value)
#             if row[39].ctype == 2:
#                 record["l2"] = str(row[39].value)
#             if row[40].ctype == 2:
#                 record["m2"] = str(row[40].value)
#             if row[42].ctype == 2:
#                 record["v3"] = str(row[42].value)
#             if row[43].ctype == 2:
#                 record["l3"] = str(row[43].value)
#             if row[44].ctype == 2:
#                 record["m3"] = str(row[44].value) 
#             if row[46].ctype == 2:
#                 record["vssn"] = str(row[46].value)
#             if row[47].ctype == 2:
#                 record["lssn"] = str(row[47].value)
#             if row[48].ctype == 2:
#                 record["mssn"] = str(row[48].value)
#     if len(record) > 0:
#         record["address"] = sum([parse_addresses(x) for x in addresses], [])
#         record["listingid"] = str(i)
#         database.insert(record)
#     database.disconnect()

# def parse_addresses(addresses):
#     addresses = addresses.split()
#     numbers = []
#     streetname = ""
#     for i in range(0, len(addresses)):
#         if addresses[i][-1] == ',':
#             numbers.append(addresses[i][:-1])
#         elif i > 0 and addresses[i-1][-1] == ',':
#             if addresses[i] == "and":
#                 continue
#             else:
#                 numbers.append(addresses[i])
#         elif i > 1 and addresses[i-1] == "and" and addresses[i-2][-1] == ',':
#             numbers.append(addresses[i])
#         elif i == 0:
#             numbers.append(addresses[i][:-1])
#         else:
#             streetname += " " + addresses[i]
#     return [i + streetname for i in numbers]
app.run()