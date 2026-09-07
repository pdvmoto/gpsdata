
import gpxpy
import oracledb
import sys

from      dotenv        import load_dotenv            
from      datetime      import datetime

from      ora_login     import *
from      prefix        import *
from      duration      import *

# ----------------------------
# Configuration
# ----------------------------
GPX_FILE_PATH = "Evening_Run.gpx"
# GPX_FILE_PATH = "tracks.gpx"
GPX_FILE_PATH="pdv_moto_10493482.gpx"

DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_DSN = "host:port/service_name"   # e.g. "localhost:1521/orclpdb"

BATCH_SIZE = 1000  # rows per executemany batch


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
                time = point.time if point.time else None
                ele = point.elevation if point.time else None
                yield (lat, lon, time, ele)


def insert_points(points, connection):
    """Insert parsed track points into the location table in batches."""
    cursor = connection.cursor()

    # typical NL values: lat = 52.5, lon=4.5
    insert_sql = """
        INSERT INTO tst_gpx ( lat, lon,                                          time,         ele )
                     VALUES (  :b1,  :b2,   to_timestamp ( :b3, 'YYYY-MM-DD HH24:MI:SS.FF' ),  :b4 )
    """

    ins_more_sql = """
      INSERT /* ins_more */ INTO 
        tst_gpx (     amount
                ,   fraction
                ,      descr
                ,        lat
                ,        lon
                ,       time
                ,        ele )
          VALUES (  :bamount
                , :bfraction
                ,    :bdescr
                ,        :b1
                ,        :b2
                ,  to_timestamp ( :b3, 'YYYY-MM-DD HH24:MI:SS.FF' )
                ,        :b4 )
    """

    batch      = []
    batch_more = []

    total_inserted = 0

    for lat, lon, time, ele in points:
        time = time.replace(tzinfo=None)
        tss = time.strftime("%Y-%m-%d %H:%M:%S.%f")
        tuple = ( lat, lon, tss, ele)
        batch.append(tuple)

        # now add some data to the batch_more record: 
        tuple_more = ( float( total_inserted / 9), float(total_inserted / 3 ), str ("desc_[" + tss + "]" ) )
        batch_more.append ( tuple_more + tuple )

        if len(batch) >= BATCH_SIZE:

            # pp ( "batch = [", batch, "]" )
            cursor.executemany(insert_sql, batch)
            total_inserted += len(batch)
            pp("Inserted rows...", total_inserted )
            # print(f"Inserted {total_inserted} rows...")

            # pp ( "batch_more = [", batch_more, "]" )
            cursor.executemany(ins_more_sql, batch_more)
            total_inserted += len(batch_more)
            print(f"more inserted {total_inserted} rows...")

            connection.commit()

            batch.clear()
            batch_more.clear()

    # insert any remaining rows
    if batch:
        cursor.executemany(insert_sql  , batch)
        cursor.executemany(ins_more_sql, batch_more)
        connection.commit()
        total_inserted += (len(batch) * 2)

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
    for lat, lon, time, ele in points:
      i += 1 
      # print ( "lat, lon, time, ele:", lat, lon, time, ele )

    print ("points printed...", i)

    try:
        connection = ora_logon ( )
    except oracledb.DatabaseError as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)

    try:
        insert_points(points, connection)
    finally:
        ora_time_spent ( connection )
        connection.close()


if __name__ == "__main__":
    main()
