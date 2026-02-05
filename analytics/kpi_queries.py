import duckdb

DB_PATH = "ev_data.duckdb"


# -------------------------
# Connexion DuckDB
# -------------------------
def get_connection():
    return duckdb.connect(DB_PATH)


# -------------------------
# Filtres - valeurs
# -------------------------
def get_brands():
    con = get_connection()
    df = con.execute(
        "SELECT DISTINCT brand FROM ev_data ORDER BY brand"
    ).df()
    con.close()
    return df["brand"].dropna().tolist()


def get_range_bounds():
    con = get_connection()
    result = con.execute(
        """
        SELECT
            MIN(range_km) AS min_range,
            MAX(range_km) AS max_range
        FROM ev_data
        WHERE range_km IS NOT NULL
        """
    ).fetchone()
    con.close()
    return int(result[0]), int(result[1])


# -------------------------
# KPI 1 : Capacité moyenne batterie
# -------------------------
def avg_battery_capacity(brand=None, min_range=None, max_range=None):
    con = get_connection()

    query = """
        SELECT AVG(battery_capacity_kWh)
        FROM ev_data
        WHERE battery_capacity_kWh IS NOT NULL
    """

    if brand:
        query += f" AND brand = '{brand}'"

    if min_range is not None and max_range is not None:
        query += f" AND range_km BETWEEN {min_range} AND {max_range}"

    result = con.execute(query).fetchone()[0]
    con.close()
    return result


# -------------------------
# KPI 2 : Top 10 marques
# -------------------------
def top_10_brands(min_range=None, max_range=None):
    con = get_connection()

    query = """
        SELECT brand, COUNT(*) AS total
        FROM ev_data
        WHERE brand IS NOT NULL
    """

    if min_range is not None and max_range is not None:
        query += f" AND range_km BETWEEN {min_range} AND {max_range}"

    query += """
        GROUP BY brand
        ORDER BY total DESC
        LIMIT 10
    """

    df = con.execute(query).df()
    con.close()
    return df


# -------------------------
# KPI 3 : Autonomie moyenne par marque
# -------------------------
def avg_range_by_brand(brand=None, min_range=None, max_range=None):
    con = get_connection()

    query = """
        SELECT brand, AVG(range_km) AS avg_range_km
        FROM ev_data
        WHERE range_km IS NOT NULL
    """

    if brand:
        query += f" AND brand = '{brand}'"

    if min_range is not None and max_range is not None:
        query += f" AND range_km BETWEEN {min_range} AND {max_range}"

    query += """
        GROUP BY brand
        ORDER BY avg_range_km DESC
    """

    df = con.execute(query).df()
    con.close()
    return df


# -------------------------
# KPI 4 : Vitesse vs Batterie
# -------------------------
def speed_vs_battery(brand=None, min_range=None, max_range=None):
    con = get_connection()

    query = """
        SELECT top_speed_kmh, battery_capacity_kWh
        FROM ev_data
        WHERE
            top_speed_kmh IS NOT NULL
            AND battery_capacity_kWh IS NOT NULL
    """

    if brand:
        query += f" AND brand = '{brand}'"

    if min_range is not None and max_range is not None:
        query += f" AND range_km BETWEEN {min_range} AND {max_range}"

    df = con.execute(query).df()
    con.close()
    return df
