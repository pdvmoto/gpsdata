print('hello yb-world, testing conn')

# import cx_Oracle


# note: had to inlcude openssl in the DYLD_LIB path in bash-profile
import psycopg2
from psycopg2 import Error

ybcon = psycopg2.connect(user="scott",
                                  password="tiger",
                                  host="127.0.0.1",
                                  port="5433",
                                  database="yugabyte")

# print (ybcon.version)

# Create a cursor to perform database operations
ybcur = ybcon.cursor()

# Print PostgreSQL details
print("PostgreSQL server information")
print(ybcon.get_dsn_parameters(), "\n")

# Executing a SQL query
ybcur.execute("SELECT version();")
# Fetch result
record = ybcur.fetchone()
print("You are connected to - ", record, "\n")

ybcon.close()
