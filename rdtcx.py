# import ggps

import xml.etree.ElementTree as ET
import json 


# Parsing an existing TCX file:
# -------------------------

# s_gpx_fname = str ( "20130330_040250.gpx" ) 
# s_tcx_fname = str ( "test_end/2012-07-29 10:20:33.0.tcx" ) 
s_tcx_fname = str ( "testend.json" ) 
# s_gpx_fname = str ( "pdv_moto_801403.gpx" )                   


# tcx_handler = ggps.GpxHandler()
# tcx_handler.parse(s_tcx_fname)

# print ( " " )
# print ( dir ( tcx_handler ) ) 
# print ( " " ) 
# hit_enter = input ( "rdtcx.py: inspect tcx_hander, press enter to continue" )

# l_trackpoint = tcx_handler.trackpoints

# print ( " " )
# print ( dir ( l_trackpoint ) ) 
# print ( " " ) 
# print ( repr ( l_trackpoint ) ) 
# print ( " len l_trackpoint:", len ( l_trackpoint ) ) 
# print ( " " ) 
# hit_enter = input ( "rdtcx.py: inspect l_trackpoint object, press enter to continue" )

# print ( " " )
# print ( " " , dir(l_trackpoint[0]))
# print ( " len l_trackpoint:", len ( l_trackpoint ) ) 
# print ( " " ) 
# hit_enter = input ( "rdtcx.py: inspect l_trackpoint [0], press enter to continue" )


print ( " ------ start json ------ " )

# tree = ET.parse( s_tcx_fname )

fl_json = open ( s_tcx_fname )
data_json = json.load( fl_json ) 

print ( dir ( data_json ) ) 
print ( " " ) 
hit_enter = input ( "rdtcx.py: inspect dir data_json , hit enter.." ) 
print ( " " ) 

print ( " " ) 
print ( repr ( data_json ) ) 
print ( " " ) 
hit_enter = input ( "rdtcx.py: inspect repr data_json, hit enter.." ) 

print ( " " ) 
print ( "rdctx.py: type, length: ", type ( data_json), len(data_json )  )
print ( " " ) 
hit_enter = input ( "rdtcx.py: type, length  data_json, hit enter.." ) 
print ( " " ) 

for js_item  in data_json:

  # print ( " " )
  #  print ( " content:" )
  # print ( "rdtcx.py: json_item :" , js_item )

  print ( " " )
  print ( " keys:" )
  print ( "rdtcx.py: json_item type :" , type ( js_item.keys() ) )
  print ( "rdtcx.py: json_item keys :" , js_item.keys() )
  s_key   = str ( js_item.keys() )
  l_key  =  list ( js_item.keys() )
  l_value = list ( js_item.values() )
  print ( "rdtcx.py: json_item s_key :" , s_key, l_key[0] ) 
  print ( "rdtcx.py: json_item values :" , js_item.values() )
  print ( "rdtcx.py: json_item values[0] :" , l_value[0] )

  print ( " " )
  # print ( " dir: " )
  # print ( dir ( js_item ) ) 
  # print ( " " )

  hit_enter = input ( "rdtcx.py: inspect js_item , hit enter.." ) 
    
  for level1 in  js_item.values():

    print ( "  level1: " , level1 ) 
    print ( "  level1:  level1-dir:",   dir ( level1 ) )
    print ( "  level1: level1-repr:",  repr ( level1 ) )
    print ( "  level1,        type:",  type ( level1 ) )

    if isinstance ( level1, list ):
      for level2 in level1:
        print ( "    level2: ", level2 )
        print ( "    level2, type: ", type ( level2 ) )
        if isinstance ( level2, list ):
          for level3 in level2:
            s_l3_key = str ( level3.keys() ) 
            print ( "      level3: type:", type ( level3 ), ", key:", s_l3_key, ", value: ", level3,   )
            if ( s_l3_key == "altitude" ):
                print ( "      level3, altitude found:", level3 )

      print ( " " )
      hit_enter = input ( "rdtcx.py: level1 was a list , hit enter.." ) 

  if ( str ( s_key ) == "points" ):
    print ( " " )
    pnts_val = js_item.values() 
    print ( " points found...", type ( pnts_val ) ) 
    print ( " points found...",        pnts_val ) 

    for pnt in pnts_val:
      print ( "Points found, pnt_val: ", pnt )

    print (" --- values printed above ---- " ) 
    print ( " " )
    hit_enter = input ( "rdtcx.py: points printed ? , hit enter.." ) 

    # end if

  # end for

# print ( data_json.points.values ) 

print ( " " )
print ( " ------ end ------ " )
print ( " " ) 

