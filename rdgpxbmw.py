
import gpxpy
import oracledb
import sys
from datetime import datetime

# ----------------------------
# Configuration
# ----------------------------
GPX_FILE_PATH = "tracks.gpx"

DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_DSN = "host:port/service_name"   # e.g. "localhost:1521/orclpdb"

BATCH_SIZE = 500  # rows per executemany batch


def parse_gpx(file_path):
    """Yield (latitude, longitude, date_time) tuples from a GPX file's trkpts."""
    with open(file_path, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat = point.latitude
                lon = point.longitude
                # point.time is a datetime (or None if the GPX has no timestamps)
                dt = point.time if point.time else None
                yield (lat, lon, dt)


def insert_points(points, connection):
    """Insert parsed track points into the location table in batches."""
    cursor = connection.cursor()

    insert_sql = """
        INSERT INTO location (id, latitude, longitude, date_time)
        VALUES (location_seq.NEXTVAL, :1, :2, :3)
    """
    # NOTE: adjust the sequence name (location_seq) to whatever your DB uses
    # for generating the id, or remove the NEXTVAL call if id is populated
    # by a trigger/identity column instead (see note below).

    batch = []
    total_inserted = 0

    for lat, lon, dt in points:
        batch.append((lat, lon, dt))
        if len(batch) >= BATCH_SIZE:
            cursor.executemany(insert_sql, batch)
            connection.commit()
            total_inserted += len(batch)
            print(f"Inserted {total_inserted} rows...")
            batch.clear()

    # insert any remaining rows
    if batch:
        cursor.executemany(insert_sql, batch)
        connection.commit()
        total_inserted += len(batch)

    cursor.close()
    print(f"Done. Total rows inserted: {total_inserted}")


def main():
    try:
        points = list(parse_gpx(GPX_FILE_PATH))
    except FileNotFoundError:
        print(f"GPX file not found: {GPX_FILE_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to parse GPX file: {e}")
        sys.exit(1)

    if not points:
        print("No track points found in GPX file.")
        return

    print(f"Parsed {len(points)} track points from GPX file.")

    i = int(0)
    for lat, lon, dt in points:
      i += 1 
      print ( "lat, lon, dt:", lat, lon, dt )

    print ("points printed...", i)

    try:
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
    except oracledb.DatabaseError as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)

    try:
        insert_points(points, connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
