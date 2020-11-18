from py.database import Database, get_listings
from googlemaps import Client as GoogleMaps

# ----------------------------------------------------------------------------------------------------------------------
def querying_location():
    database = Database()
    database.connect()
    cursor = database._connection.cursor()
    counties = []
    towns = []
    
    stmt = "SELECT listings.listingid, addresses.address, addresses.coordinates, cities.municipality, counties.county," + \
                "listings.status, listings.br1, listings.br2, listings.br3, listings.total, listings.v1, listings.v2, listings.v3, listings.l1, listings.l2," + \
                "listings.l3, listings.m1, listings.m2, listings.m3, listings.vssn, listings.lssn, listings.mssn, listings.family, listings.sr," + \
                "listings.total, listings.famsale, listings.famrent, listings.srsale, listings.srrent, listings.ssnsale, listings.ssnrent," + \
                "listings.ssn FROM listings, addresses, cities, counties WHERE listings.listingid = addresses.listingid AND " + \
                "listings.municode = cities.municode AND cities.county = counties.county"
    cursor.execute(stmt)
    
    rows = []
    ids = []

    row = cursor.fetchone()
    while row is not None:
        ids.append(row[0])
        row = list(row)
        for i in range(6, 32):
            if row[i] is None:
                row[i] = 0
        row = tuple(row)
        rows.append(row[1:])
        row = cursor.fetchone()
        
    for i in range(len(rows)):
        if rows[i][3] not in counties:
            counties.append(rows[i][3])
            
        if rows[i][2] not in towns:
            towns.append(rows[i][2])

    database.disconnect()

    return rows, ids, counties, towns
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

            print("zip code geocode success")
        except:
            print("zip is not a number")

            zipCode = None
    else:
        zipCode = None

    for i in range(len(rows)):
        flag = True

        if county != "none":
            if (rows[i][3] != county):
                print(county)
                print(rows[i][3])
                flag = False

        if town != "none":
            if (rows[i][2] != town):
                print(town)
                print(rows[i][2])
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
#            print(rows[i][2])
            addr = str(rows[i][0])
            fullAddr = addr + ", " + str(rows[i][2]) + ", " + str(rows[i][3]) + " County, NJ USA"
            coords = rows[i][1].split(',')
            x.append([float(coords[0]), float(coords[1]), ids[i], int(rows[i][8]), rows[i][5], rows[i][6], rows[i][7]])
            addressInfo.append([addr, rows[i][1], fullAddr])


    return x, addressInfo


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def query(owner, prop, bed, income, town, county, zipCode):
    database = Database()
    database.connect()
    cursor = database._connection.cursor()

#    if county is not None:
#        county = county.capitalize()
#        filtering += " AND counties.county like \'%" + county + "%\'"
#
#    if town is not None:
#        town = town.capitalize()
#        filtering += " AND cities.municipality like \'%" + town + "%\'"

    rows, ids, counties, towns = querying_location()
    x, addressInfo = filter_function(rows, ids, owner, prop, bed, income, town, county, zipCode)

    database.disconnect()

    return x, addressInfo, counties, towns, rows, ids
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def query2(owner, prop, bed, income, town, county, zipCode):
    database = Database()
    database.connect()
    cursor = database._connection.cursor()


#    if county is not None and county != '':
#        county = county.capitalize()
#        filtering += " AND counties.county like \'%" + county + "%\'"
#
#    if town is not None and town != '':
#        town = town.capitalize()
#        filtering += " AND cities.municipality like \'%" + town + "%\'"

    rows, ids, counties, towns = querying_location()
    x, addressInfo = filter_function(rows, ids, owner, prop, bed, income, town, county, zipCode)

    ids = []

    for i in range(len(x)):
        ids.append(x[i][2])

    listings_rows, listings_ids = get_listings()

    filtered_rows = []
    filtered_ids = []

    # i = 0
    # res = 0
    for i in range(len(listings_rows)):
        if listings_ids[i] in ids:
            filtered_rows.append(listings_rows[i])
            filtered_ids.append(listings_ids[i])
            # res += 1
        # i += 1


    # insert zip code filtering here !!!!

    database.disconnect()

    return filtered_rows, filtered_ids, counties, towns
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def query3(coords):
    lat = coords[0]
    long = coords[1]
    if lat == '40.0' and long == '40.0':
        map = GoogleMaps('AIzaSyAnLdUxzZ5jvhDgvM_siJ_DIRHuuirOiwQ')
        geocode_result = map.geocode(adr + ', NJ, USA')
        lat = geocode_result[0]['geometry']['location'] ['lat']
        long = geocode_result[0]['geometry']['location'] ['lng']

    return lat, long

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def html_for_listings(filtered_rows, filtered_ids):

    html = ''
    for i in range(len(filtered_rows)):
        html += '<tr><td><a href=\'details?id=' + str(filtered_ids[i]) + '\' target="_blank">' + str(filtered_rows[i][0]) + '</a></td>'
        for j in range(2, len(filtered_rows[i])):
            html += '<td>' + str(filtered_rows[i][j]) + '</td>'
        html += '</tr>'
    return html
# ----------------------------------------------------------------------------------------------------------------------
