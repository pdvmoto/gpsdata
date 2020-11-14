

import os
import sys
import glob
import zipfile
import csv
import math
import cx_Oracle
from datetime import datetime, date, time, timezone


# purpose: 
#
# - read all trips from my-adventure subdirs, into trip, gps_file and gps_line tables.
#
# history
#   2020-Nov-10, pdv, created to store records, experiment wiht py+gps data
#


# structure...
# 1.show where we are..
#
# 2. list the subdirs in order of number (name),
# 2.1 chop off nr and name, and use the data for trip-records
# 2.2 create trip record  (check for duplicate trip-nr or name ? ) 
# function:  f_madv_ins_trip ( name ), return the trip_id from oracle.

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
# 2.3.6 commit after each file or each trip => trip
# 
# 3. close down, show some statistics
# the loops/tructures above should process all files..  
# how many seconds per trip ? 
# estimated nr of lines and MB ? 


# todo:
#  - measure time, report files/sec and line/sec, to help monitor and improve speed, check
#  - consider storing absolute path, needs longer path-column
#  - consider removing hardcoded data-formats like YYYYMMDD..
#  - add checksum to gps-record? 
#  - divide over multiple sourcefiles
#  - use "struct" to read, contain, verify an RMC record
#  - try-catch error handline 
#  - When program and data are ok: load into separate schema for KEEP.
#  - add start + stop time to trip (speciic for my-adv)


# ---- some debug preparation ---- 

# take the filename, to use as prefix for print stmnts
pyfile = os.path.basename(__file__)
arg0 = sys.argv[0]
prefix=pyfile + ' '

def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp

  s_timessff = str ( datetime.now() )[11:23]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prfx, ' in function f_prfx: ' , s_prefix )

  return str ( s_prefix )

# end of f_prfx, set sourcefile and timestamp


def f_myadv_ins_trip ( s_trip ):

  # use the trip-name to insert a record and return the trip_id

  n_trip_id = int ( 1 ) 

  # print ( f_prfx(), " f_myadv_ins_trip: inserting, generate id for trip: " , s_trip )  

  s_fname    = os.path.basename ( s_trip )
  s_dirpath  = os.path.abspath ( s_fname )
  n_file_id  = int ( 1 )

  # print ( f_prfx(), " f_myadv_ins_trip: inserting, triprecord with data from " , s_dirpath, s_fname )

  sql_get_trip_id=""" select trip_seq.nextval from dual """

  cur = con.cursor()
  cur.execute ( sql_get_trip_id )
  for result in cur:
    n_trip_id = int( result[0] )

  # insert the record
  s_sql_insert = """ insert into trip ( id, trp_name )
                               values ( :1,       :2 ) """

  l_ins_values = [               n_trip_id,   s_fname ]

  print ( f_prfx(), " f_myadv_ins_trip: about to insert: " , l_ins_values )
  print ( f_prfx(), " " )

  # hit_enter = input ( f_prfx() + " f_ins_myadv_trip: about to insert trip, hit enter to continue..." )

  cur = con.cursor ()
  cur.execute ( s_sql_insert, l_ins_values )

  return n_trip_id 

# end f_myadv_ins_trip, dont include commit .. 


def f_myadv_ins_gps_file_rec ( fname ):

  # create a record for a GPS-file (RMC data) to be read, 
  # the gps_file is only an administration of incoming data, 
  # the details, points, will go into gps_line (see also ct_gprmc.sql)
  #
  # note that the file is not directly related to the trip, 
  # the relation is : gps_file -< gps_line -< trip_point  >- trip
  # a trip has trip-points, and trip-points correspond to gps_lines, 
  # thus the raw data remains close to the file+line, and is linked to trips

  s_fname    = os.path.basename ( fname )
  s_dirpath  = os.path.abspath ( fname )
  n_file_id  = int ( 1 )

  # print ( f_prfx(), " f_ins_gps_file_rec: inserting file " , fname )

  # get the seq value for n_file_id

  sql_getid1=""" select gps_file_seq.nextval from dual """

  cur = con.cursor()
  cur.execute ( sql_getid1 )
  for result in cur:
    n_file_id = int( result[0] )

  # insert the record
  s_sql_insert = """ insert into gps_file ( id,   fname,     fpath, dt_loaded )
                                   values ( :1,      :2,        :3,   sysdate ) """
  l_ins_values =                   [ n_file_id, s_fname,     fname ]

  # print ( f_prfx(), " f_ins_gps_file: about to insert: " , l_ins_values )

  cur = con.cursor ()
  cur.execute ( s_sql_insert, l_ins_values )

  return n_file_id

# end f_myadv_ins_gps_file_rec


def f_myadv_nmea_file (  n_trip_id, s_nmeafile ):
  
  # use this function to process the contents of 1 nmea file

  n_rowlen    = int ( 0 )  # length of an RMC is ...

  # some variables, GGRMC format
  n_fline     = int ( 0 )
  s_sentence  = str ( '$_____' )
  s_hmss      = str ( '000000.00' ) # time, UTC
  c_pos_stat  = str ( " " )     # validity of signal, A=ok, V=invalid
  f_lat       = float ( 0 )
  f_lon       = float ( 0 )
  c_lat_dir   = str ( ' ' )     # N or S (S=negative)
  c_lon_dir   = str ( ' ' )     # E or W (W=negative)
  f_spd       = float ( 0 )     # speed, knts
  f_trck      = float ( 0 )     # track, true, degrees
  s_date      = str ( '010170' ) # dmy,
  f_magvar    = float ( 0 )     # magnetic var, degrees
  c_vardir    = str ( ' ' )     # magnetic var, diretion, E/W
  c_mode      = str ( ' ' )     # mode indicator, Autonomous/Differential/Estimate/Manual/Notvalid

  # define the insert stmtn, 13 bind vars: 3+5+5, and a hardcoded format
  sql_ins_gps_line = """ INSERT INTO gps_line (
    gfil_id, line_nr,                                 dt
  , lat, lat_dir, lon, lon_dir, pos_status
  , speed_kn, track_true, mag_var, var_dir, mode_ind )
  VALUES ( :1,    :2, to_date ( :3, 'YYYYMMDD HH24MISS')
  ,       :4,      :5,  :6 ,      :7,         :8
  ,      :9,         :10,     :11,     :12,      :13 ) """


  n_lines_done = int ( 0 ) 
  n_lines_skipped = int ( 0 ) 
  n_file_id = int ( 0 ) 

  # print ( f_prfx(), " f_myadv_nmea_file: abt to process trip/file: " , n_trip_id, "/",  s_nmeafile )

  # create cursor once.., consider closing cursor
  cur = con.cursor()

  # create the parent record for the file, 
  n_file_id = f_myadv_ins_gps_file_rec ( s_nmeafile ) 

  # open the csv-file. and loop over the lines, count, quite a bit of code..
 
  with open ( s_nmeafile ) as csvfile:
    reader = csv.reader ( csvfile ) 
    for row in reader:

      n_rowlen = len( row ) 

      s_sentence  = row[0]
      if ( s_sentence == "$GPRMC" and n_rowlen > 12 ):

        # only count RMCs
        n_lines_done = n_lines_done + 1

        # print ( f_prfx(), " f_myadv_nmea_file: line ", n_lines_done, " Found an RMC, len=", n_rowlen )

        s_hmss      = row[1]
        c_pos_stat  = row[2]
        f_lat       = float ( row[3] + "0" )
        f_lon       = float ( row[5] + "0" )
        c_lat_dir   = row[4]
        c_lon_dir   = row[6]
        f_spd       = float ( row[ 7] + "0" )     # speed, knts
        f_trck      = float ( row[ 8] + "0" )     # track, true, degrees
        s_date      = row[9]                      # dmy,
        f_magvar    = float ( row[10] + "0" )     # magnetic var, degrees
        c_vardir    = str ( row[11]  )            # magnetic var, diretion, E/W
        c_mode      = str ( row[12][0:0]  )       # mode indicator, Autonomous/Diff/Est/Manual/Notval
        c_chksum    = str ( row[12][2:3]  )       # checksum. later.

        # now put the data in correct format and values.

        # date + time in yymmdd hhmiss
        s_oradt = "20" + s_date[4:6] + s_date [2:4] + s_date[0:2] + " " + s_hmss[0:6]

        # lat and long into decimal degrees
        f_lat = round ( math.trunc ( f_lat / 100.0 )
                        + ( ( f_lat / 100.0 ) % int(1) ) * 100 / 60
                      , 8 )

        f_lon = round ( math.trunc ( f_lon / 100.0 )
                        + ( ( f_lon / 100.0 ) % int(1) ) * 100 / 60
                      , 8 )

        # print ( f_prfx(), " f_myadv_nmea_file: some data: " 
        #  ,  s_oradt, f_lat, c_lat_dir, f_lon, c_lon_dir, f_spd, f_trck )

        # insert into, 3+5+5
        ins_values = [ n_file_id, n_lines_done, s_oradt
           , f_lat, c_lat_dir, f_lon, c_lon_dir, c_pos_stat
           , f_spd, f_trck, f_magvar, c_vardir, c_mode ]

        # cur = con.cursor ()
        cur.execute  ( sql_ins_gps_line,  ins_values )

      else:
 
        # print ( f_prfx(), "f_myadv_nmea_file :", s_sentence, " is not an RMC" )
        n_lines_skipped = n_lines_skipped + 1 

      # end-if, not an RMC line

      # print ( f_prfx(), "f_myadv_nmea_file done." )

    # end for row, reader 

  # end with

  # link the lines to the trip via trip_points
  sql_ins_points = """ insert into trip_point select gfil_id, line_nr, :1 as trp_id
                       from gps_line where gfil_id = :2 """ 
  l_points = [ n_trip_id, n_file_id ] 

  # cur = con.cursor ()
  cur.execute  ( sql_ins_points,  l_points )
  
  return n_lines_done

# end of f_myadv_nmea_file

print ( f_prfx(), ' ' ) 
print ( f_prfx(), "--- Start Main ---- " ) 
print ( f_prfx(), ' ' ) 

n_tripcount = int ( 0 ) 
n_files_total   = int ( 0 ) 
n_lines_total   = int ( 0 ) 
n_files_p_trip  = int ( 0 )
n_lines_p_trip  = int ( 0 ) 

# hardcoded locations.. and subdirs
# trips start with a number..

# s_tripdir = str ( "/Users/pdvbv/Downloads/d447c196-bfda-4c1e-ba55-265d55b5e2c4" )
s_tripdir = str ( "/Users/pdvbv/data/binsql/gpsdata/testdata" )
s_trip_subdirs = str ( "./[0-9]*" ) 
s_logdir_path = str ( "./20*_1" ) 
s_nmea_mask = str ( "*nmea.log" ) 

n_trip_id = int ( 0 ) 

s_savecwd = os.getcwd()

os.chdir ( s_tripdir ) 


con = cx_Oracle.connect('scott/tiger@127.0.0.1:1521/orclpdb1')


print ( f_prfx(), " jumped to trip-directory: ", s_tripdir ) 
print ( f_prfx(), ' ' ) 


# loop over the trips .. 

for s_trip in sorted ( glob.glob ( s_trip_subdirs ) ): 

  # print ( f_prfx(), " trip: ", s_trip, ", trip found, start processing " )

  n_tripcount = n_tripcount + 1 
  dt_trip_start = datetime.now()

  # strip the subdir to determine trip-name
  # then insert the trip in the trip-tble, based trip-name
  # 
  # Insert Trip HERE 
  n_trip_id = f_myadv_ins_trip ( s_trip )   

  n_lines_p_trip = int ( 0 ) 
  n_files_p_trip = int ( 0 ) 

  # process all "zips" or logs below the subdir
  os.chdir ( s_trip )
  for s_logdir in sorted ( glob.glob ( s_logdir_path ) ):

    # print ( f_prfx(), " logdir: ", s_logdir, " start processing logs in dir" )

    # os.chdir ( s_logdir )  

    for s_nmeafile in sorted ( glob.glob ( s_logdir + "/" + s_nmea_mask ) ) :

      # print ( f_prfx(), " nmea: ", s_nmeafile ) 

      # Process files and lines HERE
      n_files_p_trip = n_files_p_trip + 1 
      n_lines_p_trip = n_lines_p_trip + f_myadv_nmea_file (  n_trip_id, s_nmeafile )

      # print ( f_prfx(), "process, file-dir + log [", s_logdir, "/", s_nmeafile , "]" )

    # end for nmea files

    # back to parent dir.
    # os.chdir ( '..'  ) 

    # print ( f_prfx(), ' logdir: ', s_logdir, " finished processing logs in dir" )

  # end of for logdir loop

  n_lines_total = n_lines_total + n_lines_p_trip
  n_files_total = n_files_total + n_files_p_trip

  dt_trip_end = datetime.now()

  n_trip_duration_sec =  (dt_trip_end - dt_trip_start).microseconds  / 1000 
  
  print ( f_prfx(), " trip: ", s_trip, " done, files/lines:"
        , n_files_p_trip, "/", n_lines_p_trip, " totals:", n_files_total, "/", n_lines_total )
  print ( f_prfx(), " trip: ", s_trip, " took ", n_trip_duration_sec
         , "sec and did ", round ( n_lines_p_trip / n_trip_duration_sec, 3), " lines/sec" ) 
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
print ( f_prfx(), " total files   : ", n_files_total ) 
print ( f_prfx(), " total records : ", n_lines_total ) 
print ( f_prfx(), " " ) 
print ( f_prfx(), " " ) 
print ( f_prfx(), "--- Finished ---- " ) 
print ( f_prfx(), " " ) 


