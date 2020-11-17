# import ggps

import xml.etree.ElementTree as ET

# Parsing an existing TCX file:
# -------------------------

# s_gpx_fname = str ( "20130330_040250.gpx" ) 
# s_tcx_fname = str ( "test_end/2012-07-29 10:20:33.0.tcx" ) 
s_tcx_fname = str ( "test_end/first.tcx" ) 
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


print ( " ------ start xml ------ " )

tree = ET.parse( s_tcx_fname )
root = tree.getroot()
print ( dir ( tree ) ) 

print ( dir ( root ) ) 

print ( root.items() ) 
print ( root.iter('trainingcenterdatabase') ) 


for level1 in root:
  print ( " " )
  print ( " level 1 tag, attrib:" )
  print ( "tag, atrib: ", level1.tag, level1.attrib )
  print ( " " )
  print ( dir(level1) )
  print ( dir(level1.attrib) )
  print ( "keys: ", level1.attrib.keys() )
  print ( "values: ", level1.attrib.values() )
  print ( "items: ", level1.attrib.items )


  hit_enter = input ( "rdtcx.py: inspect level1 , hit enter.." ) 
    


print ( " ------ end ------ " )
print ( " " ) 

