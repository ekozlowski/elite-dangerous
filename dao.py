


# Star systems - Given on FSD jumps:
# { "timestamp":"2016-06-10T14:35:00Z", "event":"FSDJump", "StarSystem":"HIP 78085", "StarPos":[120.250,40.219,268.594], "JumpDist":36.034 }
# Also given on "Location" events:
# { "timestamp":"2016-06-10T14:32:15Z", "event":"Location", "StarSystem":"Asellus Primus", "StarPos":[-23.938,40.875,-1.344] }
# "Docked" events give us our present location:
#{ "timestamp":"2016-06-10T14:32:16Z", "event":"Docked", "StationName":"Beagle 2 Landing", "StationType":"Coriolis" }


def get_connection():
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = sqlite3.connect("./market_data.db")
    return CONNECTION

def execute_query(sql, params):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (params,))
    return cur.fetchall()

def execute_sql(sql):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


INITIAL_SQL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS StarSystem (
        StarSystem TEXT NOT NULL,
        SystemAddress INTEGER,
        x_pos REAL,
        y_pos REAL,
        z_pos REAL
    )""",
    """CREATE TABLE IF NOT EXISTS station (
        station_name TEXT NOT NULL,
        station_type TEXT NOT NULL,
        star_system TEXT NOT NULL,
        market_id INTEGER NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS market (
        id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        item_category TEXT NOT NULL,
        buy_price INTEGER NOT NULL,
        sell_price INTEGER NOT NULL,
        mean_price INTEGER NOT NULL,
        stock_bracket INTEGER NOT NULL,
        demand_bracket INTEGER NOT NULL,
        stock INTEGER NOT NULL,
        demand INTEGER NOT NULL,
        consumer BOOLEAN NOT NULL,
        producer BOOLEAN NOT NULL,
        rare BOOLEAN NOT NULL
    )
    """
    ]

CONNECTION = None

class StarSystems:

    def get_id(self, system_name):
        sql = """
        SELECT StarSystem FROM StarSystem
        WHERE StarSystem = ?
        """
        system_id = execute_query(sql, system_name)
        if system_id:
            return system_id[0][0]
        else:
            return None


    def update_from_docked_event(self, event):
        # things relevant to me:
        # StarSystem (name)
        # SystemAddress (id?)
        sql = """

        """

def update_on_docked_event(event):
    # Example data:
    """
    { "timestamp":"2018-03-07T12:22:25Z", "event":"Docked", "StationName":"Jenner Orbital", "StationType":"Outpost",
"StarSystem":"Luhman 16", "SystemAddress":22960358574928, "MarketID":3228883456, "StationFaction":"Union of
Luhman 16 Values Party", "FactionState":"CivilWar", "StationGovernment":"$government_Democracy;",
"StationGovernment_Localised":"Democracy", "StationAllegiance":"Federation", "StationServices":[ "Dock", "Autodock",
"BlackMarket", "Commodities", "Contacts", "Exploration", "Missions", "Outfitting", "CrewLounge", "Rearm", "Refuel",
"Workshop", "MissionsGenerated", "FlightController", "StationOperations", "Powerplay", "SearchAndRescue" ],
"StationEconomy":"$economy_Refinery;", "StationEconomy_Localised":"Refinery", "StationEconomies":[ {
"Name":"$economy_Refinery;", "Name_Localised":"Refinery", "Proportion":0.760000 }, { "Name":"$economy_Extraction;",
"Name_Localised":"Extraction", "Proportion":0.240000 } ], "DistFromStarLS":10.061876 }
    :param event:
    :return:
    """
    sql = """

    """

def get_connection():
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = sqlite3.connect("./market_data.db")
    return CONNECTION


def execute_sql(sql):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


for sql in INITIAL_SQL_STATEMENTS:
    execute_sql(sql)
