
## testins.py: demo insert stmtns

# ---------
#

import sys
import csv
import os
import math
import cx_Oracle
from datetime import datetime, date, time, timezone


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

pyfile = str ( os.path.basename(__file__) )
arg0 = sys.argv[0]
prefix = str ( pyfile + ' ' )

def f_prefix():

  # set a prefix for debug-output, sourcefile + timestamp

  # s_prefix = pyfile + ': '
  s_timessff = str ( datetime.now() )[11:]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prefix, ' in function f_prefix: ' , s_prefix )

  return str ( s_prefix )

# end of f_prefix, set sourcefile and timestamp


print ( f_prefix(), 'Starting... ----------- ' )

print ( f_prefix(), srcfile, ' = the srcfile' )
print ( f_prefix(), 'arg0 = [' + arg0 + '] ' )
print ( f_prefix(), ' --- ' )

# -------------- open connection ----------------

con = cx_Oracle.connect('scott/tiger@127.0.0.1:1521/orclpdb1')

cur = con.cursor()

# try an exec immedaite to create table, to test some insertions
sql_create = """
declare
  vc_sql varchar2(1000) ; 
begin

  vc_sql := ' create table cx_ora_test ( id number , name varchar2(64) , dt   date) ' ; 

 execute immediate vc_sql ; 

end;
""" 

# this could fail if table exists
# cur.execute ( sql_create ) 

con.commit()

ins1=""" insert /* marker ins1 */ 
         into cx_ora_test ( id, name,           dt ) 
         values (           :1,   :2, to_date ( :3, 'YYYYMMDD')  ) """

ins1_values = [ float (1), str ( "name" ) , str ( "20200101" ) ] 

print ( f_prefix(), ins1 ) 
print ( f_prefix(), ins1_values ) 

cur.execute ( ins1, ins1_values ) 

con.commit ()

ins2=""" insert /* marker ins2 */ 
         into cx_ora_test ( id, name,           dt ) 
         values (           :1,   :2, to_date ( :3, :4 )  ) """


n_id        = float ( 2 ) 
s_name      = str ( "2ndname" )
s_dt        = str ( "20200131 151617" )
s_dt_fmt    = str ( "YYYYMMDD HH24MISS" )


ins2_values = [ n_id, s_name, s_dt, s_dt_fmt  ] 

cur.execute ( ins2, ins2_values ) 

con.commit ()

print ( f_prefix(), ' --- the end --- ' ) 
print ( ' ' )

