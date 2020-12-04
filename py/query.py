from py.database import Database
from googlemaps import Client as GoogleMaps
from urllib.parse import quote_plus

# ----------------------------------------------------------------------------------------------------------------------
def querying_location():
    database = Database()
    database.connect()
    rows, ids = database.get_location()
    counties = set()
    towns = set()
    for i in range(len(rows)):
        counties.add(rows[i][3])
        towns.add(rows[i][2])

    database.disconnect()
    
    return rows, ids, list(counties), list(towns)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

def filter_function(rows, ids, owner, prop, bed, income, town, county, zipCode):
    x = []
    flag = True
    addressInfo = []


    if ((zipCode is not None) and (zipCode != '')):
        mapVar = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')
        zipLat = 40.0
        zipLong = 40.0

        try:
            geocode_result = mapVar.geocode(zipCode)
            zipLat = geocode_result[0]['geometry']['location'] ['lat']
            zipLong = geocode_result[0]['geometry']['location'] ['lng']
        except:
            zipCode = None
    else:
        zipCode = None

    for i in range(len(rows)):
        flag = True

        if county != "none":
            if (rows[i][3] != county):
                flag = False

        if town != "none":
            if (rows[i][2] != town):
                flag = False

        if bed is not None:
            if income is not None:
                if ((bed == "1") & (income == "very") & (rows[i][9] == 0)) or ((bed == "1") & (income == "low") & (rows[i][12] == 0)) or ((bed == "1") & (income == "moderate") & (rows[i][15] == 0)) :
                    flag = False

                if ((bed == "2") & (income == "very") & (rows[i][10] == 0)) or ((bed == "2") & (income == "low") & (rows[i][13] == 0)) or ((bed == "2") & (income == "moderate") & (rows[i][16] == 0)) :
                    flag = False

                if ((bed == "3+") & (income == "very") & (rows[i][11] == 0)) or ((bed == "3+") & (income == "low") & (rows[i][14] == 0)) or ((bed == "3+") & (income == "moderate") & (rows[i][17] == 0)) :
                    flag = False
            if ((bed == "1") & (rows[i][5] == 0)) or ((bed == "2") & (rows[i][6] == 0)) or ((bed == "3+") & (rows[i][7] == 0)):
                flag = False

        if income is not None:
            if ((income == "very") & ((rows[i][9] + rows[i][10] + rows[i][11]) == 0)) or ((income == "low") & ((rows[i][12] + rows[i][13] + rows[i][14]) == 0)) or ((income == "moderate") & ((rows[i][15] + rows[i][16] + rows[i][17]) == 0)):
                flag = False

        if owner is not None:
            if prop is not None:
                if ((owner == "rent") & (prop == "family") & (rows[i][25] == 0)) or ((owner == "rent") & (prop == "senior") & (rows[i][27] == 0)):
                    flag = False

                if ((owner == "buy") & (prop == "family") & (rows[i][24] == 0)) or ((owner == "buy") & (prop == "senior") & (rows[i][26] == 0)):
                    flag = False
            if ((owner == "rent") and ((rows[i][25] + rows[i][27] + rows[i][29]) == 0)) or ((owner == "buy") and ((rows[i][24] + rows[i][26] + rows[i][28]) == 0)):
                flag = False

        if prop is not None:
            if ((prop == "family") & (rows[i][21] == 0)) or ((prop == "senior") & (rows[i][22] == 0)):
                flag = False

        if (zipCode is not None):
            houseLat, houseLong = rows[i][1].split(',')
            houseLat = float(houseLat)
            houseLong = float(houseLong)
            if ((houseLat >= (zipLat + 0.05)) or (houseLat <= (zipLat - 0.05)) or (houseLong >= (zipLong + 0.05)) or (houseLong <= (zipLong - 0.05))):
                flag = False

        if flag == True:
            addr = str(rows[i][0])
            fullAddr = addr + ", " + str(rows[i][2]) + ", " + str(rows[i][3]) + " County, NJ"
            coords = rows[i][1].split(',')
            x.append([float(coords[0]), float(coords[1]), ids[i], int(rows[i][8]), rows[i][5], rows[i][6], rows[i][7]])
            addressInfo.append([addr, rows[i][1], fullAddr])


    return x, addressInfo


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def map_query(owner, prop, bed, income, town, county, zipCode):
    rows, ids, counties, towns = querying_location()
    x, addressInfo = filter_function(rows, ids, owner, prop, bed, income, town, county, zipCode)
    return x, addressInfo, counties, towns, rows, ids
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def listings_query(owner, prop, bed, income, town, county, zipCode):

    rows, ids, counties, towns = querying_location()
    x, addressInfo = filter_function(rows, ids, owner, prop, bed, income, town, county, zipCode)

    ids = []

    for i in range(len(x)):
        ids.append(x[i][2])

    database = Database()
    database.connect()
    listings_rows, listings_ids = database.get_listings()
    database.disconnect()

    filtered_rows = []
    filtered_ids = []

    for i in range(len(listings_rows)):
        if listings_ids[i] in ids:
            filtered_rows.append(listings_rows[i])
            filtered_ids.append(listings_ids[i])

    return filtered_rows, filtered_ids, counties, towns
# ----------------------------------------------------------------------------------------------------------------------


