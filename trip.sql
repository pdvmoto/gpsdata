
column trpnr format A20 
column trpnm format A20 

select id  
, instr ( trp_name, '_' ) pos
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( trp_name, instr ( trp_name, '_' )+1, length ( trp_name) ) as trpnm
 from trip ; 

-- min/max of trip, add to trip-info
select t.id
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) as trpnm
, count (*) nr_lines
, min (dt) earliest, max ( dt) latest 
from trip t 
   , gps_line l
   , trip_point tp
where 1=1
  and tp.gfil_id = l.gfil_id 
  and tp.line_nr = l.line_nr
  and tp.trp_id  = t.id
  and trp_name like '137_OUG%2016'
group by 
  t.id
, t.trp_name
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) 
order by 5 
;

-- points, coordinates of trip
-- optional: draw 1 line per hour, with placemarks at start of hr ?
select t.id
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) as trpnm
-- , count (*) nr_lines
-- , min (dt) earliest, max ( dt) latest 
, to_char ( l.dt, 'YYYY MON DD HH24:MI:SS' ) 
, lat, lon
from trip t 
   , gps_line l
   , trip_point tp
where 1=1
  and tp.gfil_id = l.gfil_id 
  and tp.line_nr = l.line_nr
  and tp.trp_id  = t.id
  and trp_name like '137_OUG%2016'
order by l.dt  
;

