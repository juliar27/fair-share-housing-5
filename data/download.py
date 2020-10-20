import xlwt
from data.database import Database

def download(filename):
    database = Database()
    database.connect()
    rows = database.get_excel()
    database.disconnect()

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Listings')

    # Add column headers
    columns = ["UNIQUEID", "Municode", "Municipality", "County", "Region", "SiteProgramName", 
    "ProjectDeveloper", "ComplianceMechanism", "Address", "Status", "OverallTotalUnits",
    "TotalFamily", "FamilyForSale",	"FamilyRental",	"TotalSenior", "SeniorForSale",
    "SeniorRental",	"SSNForSale", "SSNRental", "OneBRTotal", "OneBRVLI",
    "OneBRLow",	"OneBRMod",	"TwoBRTotal", "TwoBRVLI", "TwoBRLow", "TwoBRMod",	
    "ThreeBRTotal",	"ThreeBRVLI", "ThreeBRLow",	"ThreeBRMod", "SSNTotal", "SSNBRVLI",
    "SSNBRLow",	"SSNBRMod",	"Total Very Low Income Units", "Total Low-Income Units",
    "Total Moderate-Income Units", "Rental", "For Sale"]

    for i in range(0, len(columns)):
        ws.write(0, i, columns[i], xlwt.easyxf("font: bold on"))
    
    for i in range(0, len(rows)):
        for j in range(0, len(rows[i])):
            ws.write(i + 1, j, rows[i][j])

    wb.save(filename)

if __name__ == "__main__":
    download()