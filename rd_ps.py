# import data from polarstaps: mainly location-json strings with epoch

############
#
# comments, design, struture, layout here...
# 1. use some debug-stuff from other py sources..
# 2. open json file
# 2a. verify it is the data we want.. e.g. locations, and time/lat/lon
# 3. examine and list the contents in loop
# 4. generate a kml with lines (or store it in a DB..)
#
############

import xml.etree.ElementTree as ET
import json 


# import some...

import os
import sys
import glob
import math
from datetime import datetime, date, time, timezone

# import cx_Oracle
# import gpxpy
# import gpxpy.gpx


# constants, like data-directory, masks.

# take the filename, to use as prefix for print- and trace-stmnts
pyfile = os.path.basename(__file__)

# the file to read, for the moment.. 
# s_json_fname = str ( "testloc.json" ) 
s_json_fname = str ( "locations.json" ) 


# functions:
# f_prfx
# f_ins_trip, create trip-record and return trip_id
# f_ins_gps_file_rec, create file_record and return file_id
# f_runk_do_gpx,  process gpx-file, return nr-points added


# ------------------------------------------------
def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp

  s_timessff = str ( datetime.now() )[11:23]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prfx, ' in function f_prfx: ' , s_prefix )

  return str ( s_prefix )

# end of f_prfx, set sourcefile and timestamp



print ( f_prfx(), " -------- Starting -------- " ) 

print ( f_prfx(), " ------ start opening and reding json ------ " )

# tree = ET.parse( s_tcx_fname )  # this was for XML-data

fl_json = open ( s_json_fname )
data_json = json.load( fl_json ) 

print ( " " ) 
print ( f_prfx(), " file opened, and data_json object now loaded. " ) 

print ( " " ) 
print ( f_prfx(), "type: ", type ( data_json), ", length: ", len(data_json )  )
print ( " " ) 
hit_enter = input ( f_prfx() + " type, length  data_json, hit enter.." ) 
print ( " " ) 

print ( f_prfx(), " the dir of data_json: " ) 
print ( dir ( data_json ) ) 
print ( " " ) 
hit_enter = input ( f_prfx() + "rdtcx.py: inspect dir data_json , hit enter.." ) 
print ( " " ) 

print ( f_prfx(), " the repr of data_json: " ) 
print ( repr ( data_json ) ) 
print ( " " ) 
hit_enter = input ( f_prfx() + "rdtcx.py: inspect repr data_json, hit enter.." ) 

print ( " " ) 

# get the locations from the top-json object
js_locs = data_json.get ('locations') 

print ( f_prfx(), "js_locs: ", js_locs )
print ( f_prfx(), "js_locs type  : ", type (js_locs ) )
print ( f_prfx(), "js_locs length: ",  len (js_locs ) )
print ( f_prfx(), "js_locs dir   : ",  dir (js_locs ) )
print ( " " ) 

print ( f_prfx(), " inspected js_locs, about to go loop over... " ) 
hit_enter = input ( f_prfx() + "about to go loop...., hit enter.." ) 
print ( " " ) 

print ( " " )
print ( f_prfx(), " first element, js_locs[0] = " , js_locs[0] )
print ( " " )
print ( f_prfx(), " time of first element, js_locs[0].get ( 'time' )  = " , js_locs[0].get ( 'time' )  )
print ( " " )
hit_enter = input ( f_prfx() + "item[0]  ...., hit enter.." ) 


# sort. lambda... try sorting on the time-element.
# this is Really Clever..
js_locs_sorted = sorted(js_locs,  key=lambda x: x.get( 'time' ) ) 

for js_item  in js_locs_sorted:

  # print ( " " )
  # print ( f_prfx(), "js_item in data_json :" )

  # print ( f_prfx(), "js_item       :" , js_item )
  # print ( f_prfx(), "js_item dir   :" ,  dir ( js_item ) )
  # print ( f_prfx(), "js_item type  :" , type ( js_item ) )
  # print ( f_prfx(), "js_item repr  :" , repr ( js_item ) )
  # print ( f_prfx(), "js_item keys  :" , repr ( js_item.keys() ) )
  # print ( f_prfx(), "js_item items :" , repr ( js_item.items() ) )
  # print ( " " )

  # hit_enter = input ( f_prfx() + "inspect js_item , hit enter.." ) 

  # print ( " " )

  # print ( " keys:" )
  # print ( "rdtcx.py: json_item type :" , type ( js_item.keys() ) )
  # s_keys   = str ( js_item.keys() )
  # l_keys  =  list ( js_item.keys() )
  # l_value = list ( js_item.values() )
  # print ( f_prfx(), "js_item s_keys/0:" , s_keys, "key0: ", l_keys[0] ) 
  # print ( f_prfx(), "js_item values  :" , js_item.values() )
  # print ( f_prfx(), "js_item l_value :" , l_value )
  # print ( f_prfx(), "js_item values[0]:", l_value[0] )

  # print ( " " )
  # hit_enter = input ( f_prfx() + "inspect js_item, contents , hit enter.." ) 
  # print ( " " )

  n_epochtime = js_item.get ( 'time' ) 
  n_lat = round ( js_item.get ( 'lat' ) , 6 )
  n_lon = round ( js_item.get ( 'lon' ) , 6 )
  print ( n_lon, ",", n_lat, ", 0 " ) 

  # print ( f_prfx(), "tim, lat, lon", n_epochtime, n_lat, n_lon ) 
  # print ( " " )
  # hit_enter = input ( f_prfx() + "inspect tim/lat/lon, contents , hit enter.." ) 

  # loop over values if needed
  # for level1 in  js_item.values():
    # print ( f_prfx(), "  level1: " , level1 )
    # end for level1

  # end for js_item

  
# print ( data_json.points.values ) 

print ( f_prfx(), " " )
print ( f_prfx(), " ------ end ------ " )
print ( f_prfx(), " " ) 

