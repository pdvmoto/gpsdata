
# inspect a python object:
#
# show type, dir, length, rep, and more..

# constants, like data-directory, masks.

# take the filename, to use as prefix for print- and trace-stmnts


# functions: 
# f_inspset

# ------------------------------------------------
def f_inspect_obj( s_objname, o_obj ):

  print ( f_prfx(), "Object :", s_objname )

  print ( f_prfx(), "o_obj: [", o_obj, "]" )
  print ( f_prfx(), "o_obj type  : ",  type (o_obj ) )
  print ( f_prfx(), "o_obj length: ",  len (o_obj ) )
  print ( f_prfx(), "o_obj dir   : ",  dir (o_obj ) )
  print ( f_prfx(), "o_obj repr  : ",  repr ( o_obj ) ) 
  print ( " " ) 

  print ( f_prfx(), " inspected o_obj, about to go backr... " ) 
  hit_enter = input ( f_prfx() + "about to go back...., hit enter.." ) 
  print ( " " ) 

# end of f_inspect_obj, show properties of an object

