

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


print ( f_prfx(), ' ' ) 
print ( f_prfx(), "--- Start Main ---- " ) 
print ( f_prfx(), ' ' ) 

# hardcoded locations.. and subdirs
# trips start with a number..

s_tripdir = str ( "/Users/pdvbv/Downloads/d447c196-bfda-4c1e-ba55-265d55b5e2c4" )
s_trip_subdirs = str ( "./[0-9]*" ) 
s_logdir_path = str ( "./20*_1" ) 

s_savecwd = str ( "." ) 

s_savecwd = os.getcwd()

os.chdir ( s_tripdir ) 


print ( f_prfx(), " jumped to trip-directory: ", s_tripdir ) 
print ( f_prfx(), ' ' ) 


# list the trips .. 

for s_trip in sorted ( glob.glob ( s_trip_subdirs ) ): 
  print ( f_prfx(), " trip: ", s_trip, ", start processing trip found " )

  # strip the subdir to determine trip-name

  # process all zips or logs below the subdir
  os.chdir ( s_trip )
  for s_logdir in sorted ( glob.glob ( s_logdir_path ) ):

    # print ( f_prfx(), " logdir: ", s_logdir, " start    processing logs in dir" )

    os.chdir ( s_logdir )  

    for s_nmeafile in sorted ( glob.glob ( '*nmea.log' ) ) :

      # print ( f_prfx(), " nmea: ", s_nmeafile ) 
      
      print ( f_prfx(), "process, file-dir + log [", s_logdir, "/", s_nmeafile , "]" )

    # end for nmea files

    # back to parent dir.
    os.chdir ( '..'  ) 

    # print ( f_prfx(), ' logdir: ', s_logdir, " finished processing logs in dir" )

  # print ( f_prfx(), " trip: ", s_trip, " finished processing trip  " )
  
  # back to dir with all trips
  os.chdir ( s_tripdir ) 

# end-for, loop over all trips

print ( f_prfx(), " finished processing all files in directory: ", s_tripdir ) 

# at the end, renturn to thew original directory

os.chdir ( s_savecwd ) 

print ( f_prfx(), " " ) 
print ( f_prfx(), "--- Finished ---- " ) 
print ( f_prfx(), " " ) 


