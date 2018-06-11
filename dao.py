
import sqlite3

# Star systems - Given on FSD jumps:
# { "timestamp":"2016-06-10T14:35:00Z", "event":"FSDJump", "StarSystem":"HIP 78085", "StarPos":[120.250,40.219,268.594], "JumpDist":36.034 }
# Also given on "Location" events:
# { "timestamp":"2016-06-10T14:32:15Z", "event":"Location", "StarSystem":"Asellus Primus", "StarPos":[-23.938,40.875,-1.344] }
# "Docked" events give us our present location:
#{ "timestamp":"2016-06-10T14:32:16Z", "event":"Docked", "StationName":"Beagle 2 Landing", "StationType":"Coriolis" }

CONNECTION = None
def get_connection():
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = sqlite3.connect("./elite.db")
    return CONNECTION

def execute_query(sql, *args):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, args)
    print("returning cur.fetchall")
    return cur.fetchall()

def execute_sql(sql, *args):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    print("conn just committed.")


INITIAL_SQL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS StarSystem (
        StarSystem TEXT NOT NULL,
        SystemAddress INTEGER,
        x_pos REAL,
        y_pos REAL,
        z_pos REAL
    )""",
    """CREATE TABLE IF NOT EXISTS Station (
        StarSystem TEXT NOT NULL,
        StationName TEXT NOT NULL,
        StationType TEXT,
        MarketID INTEGER
    )""",
    """CREATE TABLE IF NOT EXISTS Items (
        MarketID INTEGER NOT NULL,
        ItemID INTEGER NOT NULL,
        NameLocalised TEXT,
        CategoryLocalised TEXT,
        BuyPrice INTEGER,
        SellPrice INTEGER,
        MeanPrice INTEGER,
        StockBracket INTEGER,
        DemandBracket INTEGER,
        Stock INTEGER,
        Demand INTEGER,
        Consumer BOOLEAN,
        Producer BOOLEAN,
        Rare BOOLEAN
    )
    """
    ]

def update_items(market_id, items):
    for item in items:
        item_id = item.get('id')
        name_localised = item.get('Name_Localised')
        print(f"Updating item {market_id}, {item_id}, {name_localised}")
        q = """SELECT MarketID, ItemID, NameLocalised 
 FROM Items 
 WHERE MarketID = ?
 AND ItemID = ?
 AND NameLocalised = ?"""
        data = execute_query(q, market_id, item.get('id'), item.get('Name_Localised'))
        if data:
            print("Was data")
            q = """UPDATE Items SET
        CategoryLocalised = ?,
        BuyPrice = ?,
        SellPrice = ?,
        MeanPrice = ?,
        StockBracket = ?,
        DemandBracket = ?,
        Stock = ?,
        Demand = ?,
        Consumer = ?,
        Producer = ?,
        Rare = ?
        WHERE MarketId = ?
        AND ItemID = ?
        AND NameLocalised = ?"""
            execute_sql(q,
                        item.get('Category_Localised'),
                        item.get('BuyPrice'),
                        item.get('SellPrice'),
                        item.get('MeanPrice'),
                        item.get('StockBracket'),
                        item.get('DemandBracket'),
                        item.get('Stock'),
                        item.get('Demand'),
                        item.get('Consumer'),
                        item.get('Producer'),
                        item.get('Rare'),
                        market_id,
                        item.get('id'),
                        item.get('Name_Localised')
            )
        else:
            print("Was not data")
            q = """INSERT INTO Items (
MarketID,
ItemID,
NameLocalised,
CategoryLocalised,
BuyPrice,
SellPrice,
MeanPrice,
StockBracket,
DemandBracket,
Stock,
Demand,
Consumer,
Producer,
Rare
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            execute_sql(q,
                        market_id,
                        item.get('id'),
                        item.get('Name_Localised'),
                        item.get('Category_Localised'),
                        item.get('BuyPrice'),
                        item.get('SellPrice'),
                        item.get('MeanPrice'),
                        item.get('StockBracket'),
                        item.get('DemandBracket'),
                        item.get('Stock'),
                        item.get('Demand'),
                        item.get('Consumer'),
                        item.get('Producer'),
                        item.get('Rare')
                        )
        print("done updating item")


def update_star_system(star_system, system_address, x_pos, y_pos, z_pos):
    print(f"Updating star system {star_system}")
    q = """SELECT StarSystem from StarSystem WHERE StarSystem = ?"""
    data = execute_query(q, star_system)
    if data:
        print("Was data")
        q = """UPDATE StarSystem 
SET SystemAddress = ?, x_pos = ?, y_pos = ?, z_pos = ?
WHERE StarSystem = ?"""
        execute_sql(q, system_address, x_pos, y_pos, z_pos, star_system)
    else:
        print("Was not data")
        q = """INSERT INTO StarSystem (StarSystem, SystemAddress, x_pos, y_pos, z_pos)
VALUES (?, ?, ?, ?, ?)"""
        execute_sql(q, star_system, system_address, x_pos, y_pos, z_pos)
    print("done updating star system")


def update_station(star_system, station_name, station_type, market_id):
    print(f"Updating station {station_name}")
    q = """SELECT StationName from Station WHERE StarSystem = ? AND StationName = ?"""
    data = execute_query(q, star_system, station_name)
    if data:
        print("Was data")
        q = """UPDATE Station
SET StationType = ?, MarketID = ?
WHERE StarSystem = ? AND StationName = ?"""
        execute_sql(q, station_type, market_id, star_system, station_name)
    else:
        print("Was not data")
        q = """INSERT INTO Station (StarSystem, StationName, StationType, MarketID)
VALUES (?, ?, ?, ?)"""
        execute_sql(q, star_system, station_name, station_type, market_id)
    print("done updating station")



def get_star_systems_within_radius(star_system, radius):
    data = execute_query("SELECT x_pos, y_pos, z_pos FROM StarSystem where StarSystem = ?", star_system)
    if data:
        x_pos, y_pos, z_pos = data[0]
        query = f"""
        SELECT StarSystem from StarSystem
        WHERE x_pos > ({x_pos} - {radius})
        AND x_pos < ({x_pos} + {radius})
        AND y_pos > ({y_pos} - {radius})
        AND y_pos < ({y_pos} + {radius})
        AND z_pos > ({z_pos} - {radius})
        AND z_pos < ({z_pos} + {radius})
        """
        data = execute_query(query)
        if data:
            return data
    else:
        return None


for sql in INITIAL_SQL_STATEMENTS:
    execute_sql(sql)

radius = 10
star_systems = get_star_systems_within_radius("Hsinga", radius)
if star_systems is None:
    print("No star systems found... :( ")
else:
    print(len(star_systems), f"known star systems are within {radius} LY")
    for s in star_systems:
        print(s)

