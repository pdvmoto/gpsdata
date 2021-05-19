
from xml.etree import ElementTree
import json 



# s_gpx_fname = str ( "20130330_040250.gpx" ) 
# s_tcx_fname = str ( "test_end/2012-07-29 10:20:33.0.tcx" ) 
# s_tcx_fname = str ( "testend.json" ) 
# s_gpx_fname = str ( "pdv_moto_801403.gpx" )                   

s_tcx_fname = str ( "test_end/first.tcx" ) 

print ( " ------ start tcx / xml ------ " )

print ( " " ) 

with open( s_tcx_fname, 'rt') as f:
  tree = ElementTree.parse(f)

print ( " " )
print ( "got parsed tree : ", repr ( tree ) )
print ( "tree, type      : ", type ( tree ) )
print ( "tree, dir       : ", dir ( tree )  ) 
print ( " " )
hit_enter = input ( "tree printed, hit enter.." ) 
print ( " " )

for track in tree.findall('Activities' ):
  print ( "track found: ", track ) 
  print ( " " ) 
  hit_enter = input ( "tree printed, hit enter.." ) 
  print ( " " ) 


n_iter = int ( 0 ) 

for node in tree.iter():
  n_iter += 1
  print ( "node nr          :", n_iter ) 
  print ( "node type        :", type ( node ) )
  print ( "node tag         :", node.tag        , type ( node.tag) )
  print ( "node attrib      :", node.attrib     , type ( node.attrib ), len (node.attrib) )
  print ( "node keys        :", node.keys()     , type ( node.keys() ), len ( node.keys() ) )
  print ( "node repr        :", repr ( node )   , type ( repr ( node ) ) )
  print ( "node text        :", node.text       , type ( node.text  ) )
  print ( "node dir         :", dir ( node ) )
  print ( " " ) 
  hit_enter = input ( "nodes printed, type, repr of root , hit enter.." ) 


hit_enter = input ( "--- nodes printed, --, interated over tree ---- , hit enter.." ) 

# tree = ET.parse( s_tcx_fname )
root =  tree.getroot()

print ( " " ) 
print ( "opened and did getroot" )
print ( " " ) 
print ( "root type    : ", type ( root ) ) 
print ( "root, len    : ", len ( root)  )
print ( "root repr    : ", repr ( root ) ) 
print ( "root dir     : ", dir ( root ) ) 

print ( "root items   : ", root.items )
print ( "root keys    : ", root.keys() )
# 'get', 'getchildren', 'getiterator', 'insert', 'items', 'iter', 'iterfind', 'itertext', 'keys', 'makeelement', 'remove', 'set', 'tag', 'tail', 

print ( " " ) 
hit_enter = input ( "rdtcx.py: inspected root.., hit enter.." ) 
print ( " " ) 

for track in root.findall('Track' ):
  print ( "track found: ", track ) 
  print ( " " ) 
  hit_enter = input ( "track found, printed, hit enter.." ) 
  print ( " " ) 


n_itemcount = int ( 0 ) 

for xml_item  in root:

  n_itemcount += 1

  print ( " " )
  print ( "xml_item nr      :", n_itemcount, ": " )
  print ( "xml_item         :", xml_item )
  print ( "xml_item type    :", type ( xml_item ) ) 
  print ( "xml_item, len    :", len ( xml_item)  )
  print ( "xml_item repr    :", repr ( xml_item ) )
  print ( "xml_item dir     :", dir ( xml_item ) ) 
  print ( " " ) 

  # s_key   = str ( xml_item.keys() )
  # l_key  =  list ( xml_item.keys() )
  # l_value = list ( js_item.values() )
  # print ( "xml_item s_key :" , s_key, l_key[0] ) 
  # print ( "rdtcx.py: json_item values :" , js_item.values() )
  # print ( "rdtcx.py: json_item values[0] :" , l_value[0] )

  # print ( " " )
  # print ( " dir: " )
  # print ( dir ( js_item ) ) 
  # print ( " " )

  hit_enter = input ( "xml_item inspected, hit enter.." ) 
    
  for level1 in  xml_item:

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

    # end if

  hit_enter = input ( " done level1 for xml_element, hit enter.." ) 

  # end for level1

# print ( data_json.points.values ) 

print ( " " )
print ( " ------ end ------ " )
print ( " " ) 

