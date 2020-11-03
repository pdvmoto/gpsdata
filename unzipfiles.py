
# read and unzip a list of files

import os
import sys
import glob 
import zipfile
import csv
import math

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


# some parameters etc.
zipfilepath = './zips/*.zip' 
logfilepath = './logs/*.log' 

# take the filename, to use as prefix for print stmnts
pyfile = os.path.basename(__file__)
arg0 = sys.argv[0]
prefix=pyfile + ': '

print ( prefix, '---- starting ----' ) 

print ( prefix, '---- the glob dir ----' )
ziparr = glob.glob ( zipfilepath )
print(ziparr)

print ( prefix, '<----  done with  glob dir ----' )
print ( prefix, ' ' )
print ( prefix, '--- next print files one by one --- ' )

for fname in ziparr:
  print ( prefix, '[', fname , ']' )


print ( prefix, '<----  done vertical list of  os.listdir ----' )
print ( prefix, ' ' )
print ( prefix, '--- next print unzip -u files to log dir --- ' )

for fname in ziparr:
  print ( prefix, 'unzipping [', fname , ']' )

  # faster useing zipfile pkg..
  with zipfile.ZipFile( fname,"r") as zip_ref:
    zip_ref.extractall( './logs' )

  print ( prefix, ' ---  zipfile done ' , fname, ' --- ' ) 
  print ( ' ' ) 

# end for fname

# now pick up the logfiles and get the GGRMC out of them

logarr = glob.glob ( logfilepath )
for fname in logarr:
  print ( prefix, 'logfile [', fname , ']' )
  
  n_fline = 0 
  with open ( fname ) as csvfile:
    reader = csv.reader ( csvfile )   # reading
    for row in reader:
      n_fline = n_fline + 1
      print ( prefix, ' reading line ', n_fline, '[', row, ']' )
      
      # assign and process the various items...
      # for ex, try to get the date+time to oracle-format
      # and get the lat/long correct in decimal-derees and +/- sign
      # 

      s_sentence  = row[0]
      if ( s_sentence == '$GPRMC' ):
        print ( prefix, 'Found an RMC' ) 
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

        print ( prefix, 'proces ora_dt, lat, lon, speed, dir', s_oradt, f_lat, f_lon, f_spd, f_trck )


      else: 
        print ( prefix, 'line', n_fline, ' is not RMC type:', s_sentence ) 

      # end if
    # end for

# end for logarr, loop over logfiles

print ( prefix, '---- the end ---- ' ) 

