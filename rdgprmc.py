
## rdgprmc.py: reading GPS GPRMC$ records, insert into table

# ---------
#

import sys
import csv
import os
import math
import cx_Oracle

srcfile = os.path.basename(__file__)
arg0 = sys.argv[0]

bytes_in   = int ( 0  )
bytes_out  = int ( 0 )
line       = 0
bi         = 0

lat        = float ( 0 )
lon        = float ( 0 )
ele        = round ( float ( 0 ) )
tim_hhmiss = '000000'
dat_yyyymmdd = '19700101'

run_id     = int ( 1 )

print ( 'rdgprmc.py: Starting... ----------- ' )

print ( srcfile, ' = the srcfile' )
print ( arg0, ' = arg0 ' )
print ( ' --- ' )

# -------------- open connection ----------------

con = cx_Oracle.connect('scott/tiger@127.0.0.1:1521/orclpdb1')

# below code seems to work, but is 1 extra roundtrip,
# insert-returning of id didnt work??

sql_getid1="""
select position_log_seq.nextval from dual
"""
cur = con.cursor()
cur.execute ( sql_getid1 )
for result in cur:
  run_id = int( result[0] )

print ( srcfile, ': ', ' run_id=', run_id  )  # because returning didnt work??


# -------------- reading line by line -------------

results = []
with open("gprmc.csv") as csvfile:
    reader = csv.reader(csvfile) # change contents to floats
    for row in reader: # each row is a list
        results.append(row)
        line = line + 1

        if line == 1 :
          print ( srcfile, ': ', 'first line is header : ' )
          print ( row )
          bytes_out = int ( 0 )
          bytes_in  = int ( 0 )

        else:
          # print ( srcfile, ': ', line, ' = ', row  )
          # print ( row )
          # print ( srcfile, ': ', 'items 3 - 6 are : [',  row[3], '], [' , row[4], ']', row[5], row[6] )

          lat = float ( row[3] )                      # cater for E/W/N/S later.
          lon = float ( row[5] ) 
          tim_hhmiss = str ( row[1] )[0:6]     # ingnore fractions of seconds
          dat_ddmmyy = str ( row[9] )
          dt_dmyhms = str ( dat_ddmmyy + ' ' + tim_hhmiss )

          # print ( srcfile, ': ', 'l/l, dt: ', lat, ', ', lon, ', 0 ', dat_ddmmyy, tim_hhmiss )

          lat =  math.trunc ( lat / float (100.0) ) + ( ( lat / float( 100.0) ) % int(1) ) * float (100 ) / float (60) 
          lon =  math.trunc ( lon / float (100.0) ) + ( ( lon / float( 100.0) ) % int(1) ) * float (100 ) / float (60) 
          lat = round (lat, 6)
          lon = round (lon, 6 ) 

          print ( srcfile, ': ', ' lat/long/elev: ' , lat, ', ', lon, ', ', ele , dat_ddmmyy, tim_hhmiss, dt_dmyhms ) 

          sql_insert = """
          insert into position_log ( id, dt, lat, lon ) values ( :1, to_date ( :2 , 'DDMMRR HH24MISS' ) , :3, :4 )
          """
          ins_values = [ run_id, dt_dmyhms, lat, lon ] 

          cur = con.cursor ()
          cur.execute ( sql_insert, ins_values )  

          # check contents of row.
          for i in row: 
            print( srcfile, ': [',  i, ']') 

          length = len(row) 
               
          # Iterating the index 
          # same as 'for i in range(len(list))' 
          # for i in range(length): 
          for i in range(len (row ) ): 
            print( srcfile , ': ', i, row[i]) 

# end with-open.

con.commit()

print('rdgprmc.py: The End.  ----------- the end ---- ')

