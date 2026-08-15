
set heading off
set trimspool on
set pagesize 0

spool kml

select to_char ( gln.lon, '999.99999' ) || ', ' || to_char ( gln.lat, '999.99999' ), ', 0.0'
-- , trp.*, gln.* 
from trip trp
, trip_point tp
, gps_line gln
where tp.trp_id = trp.id 
and gln.gfil_id = tp.gfil_id
and gln.line_nr = tp.line_nr
and to_char ( dt, 'SS' ) like '%0'
and  trp.id = 11 --  (select max ( id ) from trip ) 
order by trp.id, gln.dt ; 

spool off
