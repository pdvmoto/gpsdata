print('hello world, testing conn')

# uploaded as demo..
import cx_Oracle
con = cx_Oracle.connect('scott/tiger@127.0.0.1/orclpdb1')
print (con.version)
con.close()
