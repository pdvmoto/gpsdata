
# purpose: read a directory of *.gpx with runkeeper files
#   create trip with runkeeper_dt, file=filename.gpx, and points from file


# structure
#
# 1. ch-dir to runkeeper dirs
#
# 2. loop over and open all gpx files
#
# 2.1 create trip and file, based on filename.
#
# 2.2 read gpx points from file and insert
# 2.2.1  track -> segment -> point
#
# 2.3 add points to trip
#
# 2.4 commit per trip, and report per-trip data
# 
# 3 report total and close

#
# todo:
# - consider moving file onces processed
# - consider some error reporting
# - fetch next val from seq, less code ??



# import some...
import os
import sys
import glob
# import csv
import math
import cx_Oracle
import gpxpy
import gpxpy.gpx
from datetime import datetime, date, time, timezone


# constants, like data-directory, masks.

# take the filename, to use as prefix for print stmnts
pyfile = os.path.basename(__file__)
 
# s_tripdir = str ( "/Users/pdvbv/Downloads/d447c196-bfda-4c1e-ba55-265d55b5e2c4" )
s_datadir   = str ( "/Users/pdvbv/data/myadv_logs/test_rk/" )
s_gpx_mask  = str ( "20*.gpx" )


# functions:
# f_prfx
# f_ins_trip, return trip_id
# f_ins_gps_file_rec, return file_id
# f_runk_do_gpx,  process gpx-file, return nr-points added

# ------------------------------------------------ 
def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp

  s_timessff = str ( datetime.now() )[11:23]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prfx, ' in function f_prfx: ' , s_prefix )

  return str ( s_prefix )

# end of f_prfx, set sourcefile and timestamp

# ------------------------------------------------ 
def f_ins_trip ( s_trip ):

  # use the trip-name to insert a record and return the trip_id

  n_trip_id = int ( 1 )

  # print ( f_prfx(), " f_ins_trip: inserting, generate id for trip: " , s_trip )

  s_fname    = os.path.basename ( s_trip )
  s_dirpath  = os.path.abspath ( s_fname )
  n_file_id  = int ( 1 )

  # print ( f_prfx(), " f_ins_trip: inserting, triprecord with data from " , s_dirpath, s_fname )

  sql_get_trip_id=""" select trip_seq.nextval from dual """

  cur = con.cursor()
  cur.execute ( sql_get_trip_id )
  for result in cur:
    n_trip_id = int( result[0] )

  # insert the record
  s_sql_insert = """ insert into trip ( id, trp_name, created_by, created_dt )
                               values ( :1,       :2,         :3,    sysdate ) """

  l_ins_values = [               n_trip_id,   s_fname,    pyfile  ]

  print ( f_prfx(), " f_ins_trip: about to insert: " , l_ins_values )
  print ( f_prfx(), " " )

  # hit_enter = input ( f_prfx() + " f_ins_trip: about to insert trip, hit enter to continue..." )

  cur = con.cursor ()
  cur.execute ( s_sql_insert, l_ins_values )

  return n_trip_id

# end f_ins_trip, dont include commit ..

# ------------------------------------------------ 
def f_ins_gps_file_rec ( fname ):

  # create a record for a GPS-file (RMC data) to be read,
  # the gps_file is only an administration of incoming data,
  # the details, points, will go into gps_line (see also ct_gprmc.sql)
  #
  # note that the file is not directly related to the trip,
  # the relation is : gps_file -< gps_line -< trip_point  >- trip
  # a trip has trip-points, and trip-points correspond to gps_lines,
  # thus the raw data remains close to the file+line, and is linked to trips
  #
  # consider this for separate sourcefile.py
  # consider: comments and more at file

  s_fname    = os.path.basename ( fname )
  s_dirpath  = os.path.abspath ( fname )
  n_file_id  = int ( 1 )

  # print ( f_prfx(), " f_ins_gps_file_rec: inserting file " , fname , s_dirpath)

  # get the seq value for n_file_id

  sql_getid1=""" select gps_file_seq.nextval from dual """

  cur = con.cursor()
  cur.execute ( sql_getid1 )
  for result in cur:
    n_file_id = int( result[0] )

  # insert the record
  s_sql_insert = """ insert into gps_file ( id,   fname,     fpath, dt_loaded )
                                   values ( :1,      :2,        :3,   sysdate ) """
  l_ins_values =                   [ n_file_id, s_fname, s_dirpath ]

  # print ( f_prfx(), " f_ins_gps_file: about to insert: " , l_ins_values )

  # cur = con.cursor ()
  cur.execute ( s_sql_insert, l_ins_values )

  return n_file_id

# end f_ins_gps_file_rec

# ------------------------------------------------ 
def f_runk_do_gpx ( n_trip_id , gpxfile ):

  # insert the points from 1 gpx file, and assign to trip
  # this includes creating the file-record,
  # and consider adding the first track name to the trip-record
  # consider debug and timing inside this function, but it is big already

  dt_file_start = datetime.now () 

  cur = con.cursor ()   # consider a global cursor object for all adhoc sql

  # define the sql-stmnt as constant, consider putting it outside
  sql_ins_line = """ insert into gps_line 
           ( gfil_id, line_nr, lat, lon,                dt )
    values (      :1,      :2,  :3,  :4, to_date ( :5,  'YYYY-MM-DD HH24:MI:SS' ) ) """

  s_ymdfmt = str ( "YYYY-MM-DD HH24:MI:SS" )

  print ( f_prfx(), " f_runk_do_gpx file ", gpxfile )
  n_tracks_done   = int ( 0 )
  n_segments_done = int ( 0 )
  n_points_done   = int ( 0 )

  # open, parse and loop over the gpx file

  # create the file-record first.
  n_file_id = int ( f_ins_gps_file_rec ( gpxfile ) )

  gpx_file = open( gpxfile, 'r')
  gpx = gpxpy.parse(gpx_file)

  for track in gpx.tracks:

    print ( " " )
    # hit_enter = input ( f_prfx() + " runk_do, abt to do track:" + track.name + " hit enter..."  )

    for segment in track.segments:
    
      for point in segment.points:

        s_dt1 = str ( point.time )   # the ora-dt is a smaller str, ..
        s_oradt = str ( s_dt1[0:19] )
        n_points_done = n_points_done + 1

        # print ( f_prfx(), " runk_do, point lat/lon, ele, time"
        # , n_points_done, point.latitude, point.longitude
        # , point.elevation, point.time , s_dt1, "[" + s_oradt + "]" ) 

        l_ins_values = [  n_file_id, n_points_done, point.latitude, point.longitude , s_oradt  ]

        # print ( f_prfx(), " runk_do, sql is: ", sql_ins_line )
        # print ( f_prfx(), " runk_do, abt to insert: ", l_ins_values )

        cur.execute ( sql_ins_line, l_ins_values ) 

      # end for points

    # end for segments

  # end for, loop over all tracks

  # assign the points to the trip_id, use 1 ins-select stmnt
  sql_ins_points = """ insert into trip_point select gfil_id, line_nr, :1 as trp_id
                       from gps_line where gfil_id = :2 """
  l_points = [ n_trip_id, n_file_id ]

  cur.execute  ( sql_ins_points,  l_points )

  # update some global statistics..
  
  # mention time
  dt_file_end = datetime.now () 
  n_file_dur_sec = ( dt_file_end - dt_file_start).microseconds / 1000000

  print ( f_prfx(), "runk_do, points, duration: ", n_points_done, n_file_dur_sec )  

  return n_points_done

# end f_runk_do_gpx ----- 


# start main

# ---- some debug preparation ----

dt_start_total = datetime.now() 

print ( f_prfx(), ' ' )
print ( f_prfx(), "--- Start Main --- ", pyfile, " ---- " )
print ( f_prfx(), ' ' )

n_trips_total   = int ( 0 )
n_files_total   = int ( 0 )

n_tracks_total  = int ( 0 ) 
n_segments_total  = int ( 0 ) 
n_points_total   = int ( 0 )

n_tracks_p_file    = int (0)
n_segments_p_file  = int ( 0 )
n_points_p_file    = int ( 0 )

n_trip_id = int ( 0 )
n_file_id = int ( 0 )

s_savecwd = os.getcwd()
os.chdir ( s_datadir )

# connection is a global-object, for use everywhere in program
con = cx_Oracle.connect('scott/tiger@127.0.0.1:1521/orclpdb1')


for gpxfile in sorted ( glob.glob ( s_gpx_mask ) ) :

  dt_start_trip = datetime.now() 

  # print ( f_prfx(), " file: ", gpxfile ) 

  n_files_total = n_files_total + 1 
  n_trip_id = f_ins_trip ( gpxfile ) 

  # call the funtion to process the runkeeper file, returns nr points
  n_points_p_file = f_runk_do_gpx ( n_trip_id , gpxfile ) 

  # at the end of each file: increase tracks, segments, points
  # note those are global variables, can be done in called-functions

  con.commit ()  # commit the trip

  n_trips_total = n_trips_total + 1  
  n_points_total = n_points_total + n_points_p_file

  dt_end_trip = datetime.now() 
  n_duration_trip_sec =  ( dt_end_trip - dt_start_trip ).microseconds / 1000000 

  print ( " " )
  
  # print ( f_prfx(), " trip start, end: ", dt_start_trip, dt_end_trip )
  print ( f_prfx(), " trip id, file  : ", n_trip_id, gpxfile , "took "
        , n_duration_trip_sec, " sec.")
  print ( f_prfx(), " trip points    : ", n_points_p_file, " at "
        , round ( n_points_p_file / n_duration_trip_sec, 2 ), " pnts/sec." ) 

# end for, looped over all gpx files


# at the end: 
# commit, close connection, ... 
# report duration, files, files/sec, points, points/sec

con.commit () 
con.close()

os.chdir ( s_savecwd )

dt_end_total = datetime.now() 

n_duration_sec = (dt_end_total - dt_start_total).microseconds  / float ( 1000000 )

print ( f_prfx(), " " )
print ( f_prfx(), " duration sec: ", n_duration_sec ) 
print ( f_prfx(), " " )
print ( f_prfx(), " -------- the end ------- " ) 



