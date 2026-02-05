import duckdb

DB_PATH = "ev_data.duckdb"

def get_connection():
    return duckdb.connect(DB_PATH)

def avg_battery_capacity():
    con = get_connection()
    query = """
        SELECT AVG(battery_capacity_kwh) AS avg_battery
        FROM ev_data
        WHERE battery_capacity_kwh IS NOT NULL
    """
    result = con.execute(query).fetchone()[0]
    con.close()
    return result

def top_10_brands():
    con = get_connection()
    query = """
        SELECT brand, COUNT(*) AS total
        FROM ev_data
        GROUP BY brand
        ORDER BY total DESC
        LIMIT 10
    """
    df = con.execute(query).df()
    con.close()
    return df

def battery_type_distribution():
    con = get_connection()
    query = """
        SELECT battery_type, COUNT(*) AS total
        FROM ev_data
        GROUP BY battery_type
        ORDER BY total DESC
    """
    df = con.execute(query).df()
    con.close()
    return df

def speed_vs_battery():
    con = get_connection()
    query = """
        SELECT max_speed_kmh, battery_capacity_kwh
        FROM ev_data
        WHERE max_speed_kmh IS NOT NULL
          AND battery_capacity_kwh IS NOT NULL
    """
    df = con.execute(query).df()
    con.close()
    return df
