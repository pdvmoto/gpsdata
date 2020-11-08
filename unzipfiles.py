 
# read and unzip a list of files

import os
import sys
import glob 
import zipfile
import csv
import math
import cx_Oracle
from datetime import datetime, date, time, timezone

# some variables, GGRMC format
n_fline     = int ( 0 ) 
s_sentence  = str ( '$_____' ) 
s_hmss      = str ( '000000.00' ) # time, UTC
c_pos_stat  = str ( " " )  # validity of signal, A=ok, V=invalid
f_lat       = float ( 0 )
f_lon       = float ( 0 ) 
c_lat_dir   = str ( ' ' )  # N or S (S=negative)
c_lon_dir   = str ( ' ' )  # E or W (W=negative)
f_spd       = float ( 0 )      # speed, knts
f_trck      = float ( 0 )     # track, true, degrees
s_date      = str ( '010170' ) # dmy, 
f_magvar    = float ( 0 )    # magnetic var, degrees
c_vardir    = str ( ' ' )    # magnetic var, diretion, E/W
c_mode      = str ( ' ' )    # mode indicator, Autonomous/Differential/Estimate/Manual/Notvalid

s_oradt     = str ( '010170T000000' ) # string to hold DT combined, mind the RR for YY

s_fname     = str ( 'filename' )
s_dirpath   = str ( '/tmp' )

# some parameters etc.
zipfilepath    = './zips/'
zipfilemask    = '*.zip' 
logfilepath    = './logs/' 
logfilemask    = '*.log'

donefilepath    = './done/' 

# take the filename, to use as prefix for print stmnts
pyfile = os.path.basename(__file__)
arg0 = sys.argv[0]
prefix=pyfile + ' '

def f_prefix():

  # set a prefix for debug-output, sourcefile + timestamp

  # s_prefix = pyfile + ': '
  s_timessff = str ( datetime.now() )[11:]  
  s_prefix = pyfile + ' ' + s_timessff + ': ' 

  # print ( prefix, ' in function f_prefix: ' , s_prefix )

  return str ( s_prefix )

# end of f_prefix, set sourcefile and timestamp

def f_ins_gps_file ( fname ):

  s_fname    = os.path.basename ( fname )
  s_dirpath  = os.path.abspath ( fname )
  n_file_id  = int ( 1 )
 
  print ( f_prefix(), ' inserting file for name ' , fname )

  # get the seq value for n_file_id

  sql_getid1="""
  select gps_file_seq.nextval from dual
  """
  cur = con.cursor()
  cur.execute ( sql_getid1 )
  for result in cur:
    n_file_id = int( result[0] )

  # insert the record
  s_sql_insert = """ insert into gps_file ( id, fname, fpath, dt_loaded ) 
    values ( :1, :2, :3, sysdate ) 
  """
  l_ins_values = [ n_file_id, s_fname, s_dirpath ] 
  
  print ( f_prefix(), 'about to insert: ' , l_ins_values )

  cur = con.cursor ()
  cur.execute ( s_sql_insert, l_ins_values )

  return n_file_id

# end f_ins_gps_file

def f_process_data_from_zip ( n_file_id, s_logfilepath ):

  # insert the lines from the logs from 1 zipfile, refer to parent n_file_id
  # assume: no other logfiles in log-dir (tricky!)

  # define the insert stmtn
  sql_ins_gps_line = """ INSERT INTO gps_line (
    gfil_id, line_nr,                                 dt
  , lat, lat_dir, lon, lon_dir, pos_status
  , speed_kn, track_true, mag_var, var_dir, mode_ind ) 
  VALUES ( :1,    :2, to_date ( :4, 'YYYYMMDD HH24MISS')
  ,       :4,      :5,  :6 ,      :7,         :8
  ,      :9,         :10,     :11,     :12,      :13 ) """

  # start processing
  # find the logfile/s, open as CSV,
  
  logarr = glob.glob ( s_logfilepath + logfilemask )
  for s_logfile in logarr:

    print ( f_prefix(), 'f_process, logfile [', s_logfile , ']' )
      
    n_lines_done = int ( 0 ) 

    with open ( s_logfile ) as csvfile:
      reader = csv.reader ( csvfile )   # reading
      for row in reader:
        n_lines_done = n_lines_done + 1
        # print ( f_prefix(), ' reading line ', n_lines_done, '[', row, ']' )
        
        # assign and process the various items...
        # for ex, try to get the date+time to oracle-format
        # and get the lat/long correct in decimal-derees and +/- sign
        # 

        s_sentence  = row[0]
        if ( s_sentence == '$GPRMC' ):
          print ( f_prefix(), 'f_process: line ', n_lines_done, ' Found an RMC' ) 
          s_hmss      = row[1] 
          c_pos_stat  = row[2]
          f_lat       = float ( row[3] )
          f_lon       = float ( row[5] ) 
          c_lat_dir   = row[4]
          c_lon_dir   = row[6]
          f_spd       = float ( row[7] )      # speed, knts
          f_trck      = float ( row[8] )      # track, true, degrees
          s_date      = row[9]                # dmy, 
          f_magvar    = float ( row[10] + '0' )    # magnetic var, degrees
          c_vardir    = str ( row[11]  )      # magnetic var, diretion, E/W
          c_mode      = str ( row[12][0:0]  )      # mode indicator, Autonomous/Diff/Est/Manual/Notval
          c_chksum    = str ( row[12][2:3]  )      # checksum. later.
   
          # now put the data in correct format and values.

          # date + time in yymmdd hhmiss
          s_oradt = '20' + s_date[4:6] + s_date [2:4] + s_date[0:2] + ' ' + s_hmss[0:6] 

          # lat and long into decimal degrees
          f_lat = round ( math.trunc ( f_lat / 100.0 ) 
                          + ( ( f_lat / 100.0 ) % int(1) ) * 100 / 60
                        , 8 )

          f_lon = round ( math.trunc ( f_lon / 100.0 ) 
                          + ( ( f_lon / 100.0 ) % int(1) ) * 100 / 60
                        , 8 )

          print ( f_prefix(), 'proces ora_dt, lat, lon, speed, dir', s_oradt, f_lat, f_lon, f_spd, f_trck )

          # insert into
          ins_values = [ n_file_id, n_lines_done, s_oradt, f_lat, c_lat_dir, f_lon, c_lon_dir, c_pos_stat
             , f_spd, f_trck, f_magvar, c_vardir, c_mode ] 

          cur = con.cursor ()
          cur.execute  ( sql_ins_gps_line,  ins_values )

        else:  # if the file was not a RMC record, skip or process otherwise
          print ( f_prefix(), 'file/line', n_file_id, '/', n_lines_done, ' is not RMC type:', s_sentence ) 

        # end if GPRMC

      # end for all lines

      # move the file so it doest get spotted again
      ( s_logfile_head, s_logfile_fname ) = os.path.split ( s_logfile ) 
      s_log_done = donefilepath + s_logfile_fname

      print ( f_prefix(), 'moving file [', s_logfile, '] to [', s_log_done, ']' )

      os.rename ( s_logfile, s_log_done )        

    # end with , end logfile done

  return n_lines_done

# end f_process_data_from_zip ----

print ( f_prefix(), '---- starting ----' ) 

# print ( f_prefix(), '---- the glob dir ----' )
ziparr = glob.glob ( zipfilepath + zipfilemask )

# print(ziparr)

# print ( f_prefix(), '<----  done with  glob dir ----' )
print ( f_prefix(), ' ' )
print ( f_prefix(), '--- next print files one by one --- ' )

for fname in ziparr:
  print ( f_prefix(), '[', fname , ']' )

print ( f_prefix(), '<----  done vertical list of  files ----' )
print ( f_prefix(), ' ' )
print ( f_prefix(), ' ' )

hit_enter = input ( prefix + 'hit enter to continue...' )

print ( f_prefix(), ' --- try getting filenames and paths --- ' )

for fname in ziparr:
  s_fname    = os.path.basename ( fname ) 
  s_dirpath  = os.path.abspath ( fname )
  s_localdir = os.path.dirname ( fname )

  print ( f_prefix(), 'file [', fname , '] and abspath [', s_dirpath, ']' )
  print ( f_prefix(), 'path and name [', s_localdir, ' - ', s_fname , ']' )

hit_enter = input ( prefix + ' path + names check, hit enter to continue...' )

# -------------- open connection ----------------

con = cx_Oracle.connect('scott/tiger@127.0.0.1:1521/orclpdb1')

print ( f_prefix(), '--- next print unzip -u files to log dir --- ' )

for fname in ziparr:

  print ( f_prefix(), 'unzipping [', fname , ']' )

  # faster useing zipfile pkg..
  with zipfile.ZipFile( fname,"r") as zip_ref:
    zip_ref.extractall( logfilepath )

  print ( f_prefix(), ' ---  unzip file done ' , fname, ' --- ' ) 
  print ( ' ' ) 

  # add record to database
  n_file_id = f_ins_gps_file ( fname ) 

  print ( f_prefix(), ' ---  file-record created for file id ', n_file_id, fname )
  
  # consider processing the extracted file/s here.. 
  f_process_data_from_zip ( n_file_id, logfilepath )
 
  con.commit()

  print ( ' ' ) 
  print ( ' ' ) 
  print ( f_prefix(), 'file: ', fname, 'unzip+processing done' ) 
  print ( ' ' ) 
  hit_enter = input ( 'file-process done, hit enter to continue...' )

# end for fname, one zipfile processed

print ( ' ' ) 
print ( ' ' ) 
hit_enter = input ( f_prefix() + 'unzip+ process done, hit enter to continue...' )

# now pick up the logfiles and get the GGRMC out of them

logarr = glob.glob ( logfilepath + logfilemask )
for fname in logarr:
  print ( f_prefix(), 'logfile [', fname , ']' )
  
  n_fline = 0 
  with open ( fname ) as csvfile:
    reader = csv.reader ( csvfile )   # reading
    for row in reader:
      n_fline = n_fline + 1
      # print ( f_prefix(), ' reading line ', n_fline, '[', row, ']' )
      
      # assign and process the various items...
      # for ex, try to get the date+time to oracle-format
      # and get the lat/long correct in decimal-derees and +/- sign
      # 

      s_sentence  = row[0]
      if ( s_sentence == '$GPRMC' ):
        # print ( f_prefix(), 'Found an RMC' ) 
        s_hmss      = row[1] 
        c_pos_stat  = row[2]
        f_lat       = float ( row[3] )
        f_lon       = float ( row[5] ) 
        c_lat_dir   = row[4]
        c_lon_dir   = row[6]
        f_spd       = float ( row[7] )      # speed, knts
        f_trck      = float ( row[8] )      # track, true, degrees
        s_date      = row[9]                # dmy, 
        f_magvar    = float ( row[10] + '0' )    # magnetic var, degrees
        c_vardir    = str ( row[11]  )      # magnetic var, diretion, E/W
        c_mode      = str ( row[12]  )      # mode indicator, Autonomous/Diff/Est/Manual/Notval
 
        s_oradt = '20' + s_date[4:6] + s_date [2:4] + s_date[0:2] + ' ' + s_hmss[0:6] 

        f_lat = round ( math.trunc ( f_lat / 100.0 ) 
                        + ( ( f_lat / 100.0 ) % int(1) ) * 100 / 60
                      , 8 )

        f_lon = round ( math.trunc ( f_lon / 100.0 ) 
                        + ( ( f_lon / 100.0 ) % int(1) ) * 100 / 60
                      , 8 )

        print ( f_prefix(), 'proces ora_dt, lat, lon, speed, dir', s_oradt, f_lat, f_lon, f_spd, f_trck )


      else: 
        print ( f_prefix(), 'line', n_fline, ' is not RMC type:', s_sentence ) 

      # end if
    # end for

# end for logarr, loop over logfiles

# commit at end, makesure zipfile + data are under 1 commit
con.commit () 

print ( prefix, '---- the end ---- ' ) 

