from py.database import Database

def get_favorite_listings(favorites):
    ids = []
    adrs = []
    for i in favorites:
        i = i.replace('%27', "\'")
        split_fav = i.split(';')
        ids.append(split_fav[0])
        adrs.append(split_fav[1])

    database = Database()
    database.connect()
    final_rows, final_ids = database.get_favorite_listings(ids, adrs)
    database.disconnect()
    return final_rows, final_ids

