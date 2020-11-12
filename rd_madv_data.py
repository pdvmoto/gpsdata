

import os
import sys
import glob
import zipfile
import csv
import math
import cx_Oracle
from datetime import datetime, date, time, timezone



# purpose: 
# - read all trips from my-adventure subdirs, into trip, gps_file and gps_line tables.


# structure...
# 1.show where we are..
#
# 2. list the subdirs in order of number (name),
# 2.1 chop off nr and name, and use the data for trip-records
# 2.2 create trip record  (check for duplicate trip-nr or name ? ) 
# function:  madv_ins_trip ( nr, name ), return the trip_id from oracle.

# 2.3 go into trip-dir, list the subdirs again... each subdir is a file
# 2.3.1 go into first dir, use dirname as filename for data to read
# 2.3.2 create the file records
#       fuctions: madv_ins_gps_file, return file_id
#     (dirname is a date+time format) 
#
# 2.3.3 go into file-dir, and open 1 or more *nmea.log files.  
#       function madv_ins_gps_lines ( trip, file_id, nmea_file_name )
# 2.3.4 use pygpx to process nmea records (for trip and file) into gps_line and trp_point
# 2.3.5 consider moving or marking each file after processing
# 2.3.6 commit after each file
# 
# the loops/tructures above should process all files..  
# how many seconds per trip ? 
# estimated nr of lines and MB ? 


# take the filename, to use as prefix for print stmnts
pyfile = os.path.basename(__file__)
arg0 = sys.argv[0]
prefix=pyfile + ' '

def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp

  # s_prefix = pyfile + ': '
  s_timessff = str ( datetime.now() )[11:]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prfx, ' in function f_prfx: ' , s_prefix )

  return str ( s_prefix )

# end of f_prfx, set sourcefile and timestamp


def f_myadv_ins_trip ( s_trip ):

  # use the trip-name to insert a record and return the trip_id

  n_trip_id = int ( 1 ) 

  print ( f_prfx(), " inserting record and generate id for trip: " , s_trip )  

  s_fname    = os.path.basename ( s_trip )
  s_dirpath  = os.path.abspath ( s_fname )
  n_file_id  = int ( 1 )

  print ( f_prfx(), " inserting trip with data from " , s_dirpath, s_fname )

  sql_get_trip_id="""
  select trip_seq.nextval from dual
  """
  cur = con.cursor()
  cur.execute ( sql_get_trip_id )
  for result in cur:
    n_trip_id = int( result[0] )

  # insert the record
  s_sql_insert = """ insert into trip ( id, trp_name )
    values ( :1, :2 )
  """
  l_ins_values = [ n_trip_id, s_trip ]

  print ( f_prfx(), " f_myadv_ins_trip: about to insert: " , l_ins_values )
  print ( f_prfx(), " " )

  hit_enter = input ( f_prfx() + " about to insert trip.. hit enter to continue..." )

  cur = con.cursor ()
  cur.execute ( s_sql_insert, l_ins_values )

  return n_trip_id 

# end f_myadv_ins_trip, dont include commit .. 


def f_myadv_nmea_file (  n_trip_id, s_nmeafile ):
  
  n_lines_done = int ( 0 ) 

  # use this function to process the contents of 1 nmea file

  # print ( f_prfx(), " f_myadv_nmea_file: abt to process trip/file: " , n_trip_id, "/",  s_nmeafile )

  # open the csv-file. and loop over the lines, count, quite a bit of code..
  

  return n_lines_done

# end of f_myadv_nmea_file

print ( f_prfx(), ' ' ) 
print ( f_prfx(), "--- Start Main ---- " ) 
print ( f_prfx(), ' ' ) 

n_tripcount = int ( 0 ) 
n_filecount = int ( 0 ) 
n_lines_p_trip  = int ( 0 ) 
n_lines_total   = int ( 0 ) 

# hardcoded locations.. and subdirs
# trips start with a number..

s_tripdir = str ( "/Users/pdvbv/Downloads/d447c196-bfda-4c1e-ba55-265d55b5e2c4" )
s_trip_subdirs = str ( "./[0-9]*" ) 
s_logdir_path = str ( "./20*_1" ) 
s_nmea_mask = str ( "*nmea.log" ) 

n_trip_id = int ( 0 ) 

s_savecwd = str ( "." ) 

s_savecwd = os.getcwd()

os.chdir ( s_tripdir ) 


con = cx_Oracle.connect('scott/tiger@127.0.0.1:1521/orclpdb1')


print ( f_prfx(), " jumped to trip-directory: ", s_tripdir ) 
print ( f_prfx(), ' ' ) 


# list the trips .. 

for s_trip in sorted ( glob.glob ( s_trip_subdirs ) ): 
  print ( f_prfx(), " trip: ", s_trip, ", start processing trip found " )

  n_tripcount = n_tripcount + 1 

  # strip the subdir to determine trip-name
  # then insert the trip in the trip-tble, based trip-name
  # HERE 
  n_trip_id = f_myadv_ins_trip ( s_trip )   

  n_lines_p_trip = int ( 0 ) 

  # process all zips or logs below the subdir
  os.chdir ( s_trip )
  for s_logdir in sorted ( glob.glob ( s_logdir_path ) ):

    # print ( f_prfx(), " logdir: ", s_logdir, " start    processing logs in dir" )

    # os.chdir ( s_logdir )  

    for s_nmeafile in sorted ( glob.glob ( s_logdir + "/" + s_nmea_mask ) ) :

      # print ( f_prfx(), " nmea: ", s_nmeafile ) 

      n_filecount    = n_filecount + 1 
      n_lines_p_trip = n_lines_p_trip + f_myadv_nmea_file (  n_trip_id, s_nmeafile )
      n_lines_total  = n_lines_total  + n_lines_p_trip 

      # print ( f_prfx(), "process, file-dir + log [", s_logdir, "/", s_nmeafile , "]" )

    # end for nmea files

    # back to parent dir.
    # os.chdir ( '..'  ) 

    # print ( f_prfx(), ' logdir: ', s_logdir, " finished processing logs in dir" )

  print ( f_prfx(), " trip: ", s_trip, " done, files/lines/total :"
        , n_filecount, "/", n_lines_p_trip, "/", n_lines_total )
  print ( f_prfx(), " " )
  
  # back to dir with all trips
  os.chdir ( s_tripdir ) 

  # commit per trip
  con.commit ()

# end-for, loop over all trips

print ( f_prfx(), " finished processing all files in directory: ", s_tripdir ) 

# at the end, renturn to thew original directory

os.chdir ( s_savecwd ) 


print ( f_prfx(), " " ) 
print ( f_prfx(), " total trips   : ", n_tripcount ) 
print ( f_prfx(), " total files   : ", n_filecount ) 
print ( f_prfx(), " total records : ", n_recordcount ) 
print ( f_prfx(), " " ) 
print ( f_prfx(), " " ) 
print ( f_prfx(), "--- Finished ---- " ) 
print ( f_prfx(), " " ) 


