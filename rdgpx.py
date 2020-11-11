import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------

s_gpx_fname = str ( "20130330_040250.gpx" ) 

gpx_file = open(s_gpx_fname, 'r')

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:

    # print ( 'track:', track )

    for segment in track.segments:

        print ( '  segment: ', segment )
        print ( '  segment: ', segment.get_time_bounds )

        for point in segment.points:
            print('    Track Point at ({0},{1}) -> ele= {2} and time= {3}'.format(point.latitude, point.longitude, point.elevation, point.time))


for waypoint in gpx.waypoints:
    print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

for route in gpx.routes:
    print('Route:')
    for point in route.points:
        print('Route Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

# There are many more utility methods and functions:

#print ( 'tracks:', gpx.tracks )
print ( 'segments of first track:', gpx.tracks[0].segments )
print ( ' ' ) 
print ( 'contents of segment[0] :', gpx.tracks[0].segments[0] )
print ( ' ' ) 
print ( 'contents of point[0] :', gpx.tracks[0].segments[0].points[0] )
print ( ' ' ) 
print ( 'points:', gpx.points )

