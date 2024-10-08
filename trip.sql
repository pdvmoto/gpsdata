
column trpnr format A8 
column trpnm format A20 
column cpcmd format A60 

select id  
, instr ( trp_name, '_' ) pos
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( trp_name, instr ( trp_name, '_' )+1, length ( trp_name) ) as trpnm
 from trip ; 

select ' ! cp aatest.kml ' 
  || substr ( trp_name, instr ( trp_name, '_' )+1, length ( trp_name) ) || '.kml' as cpcmd
from trip t
where t.id = 17 ; 


! read -t 5 -p "check the copy command " abc 

-- min/max of trip, add to trip-info
select t.id
-- , substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) as trpnm
, count (*) nr_lines
, min (dt) earliest
, max ( dt) latest 
from trip t 
   , gps_line l
   , trip_point tp
where 1=1
  and tp.gfil_id = l.gfil_id 
  and tp.line_nr = l.line_nr
  and tp.trp_id  = t.id
  -- and trp_name like '137_OUG%2016'
group by 
  t.id
, t.trp_name
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) 
order by 4 
;

! echo .
! read -t 10 -p " ^ list of trip(s) with start+end date" abc
! echo .

select t.id
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) as trpnm
, to_char ( trunc ( l.dt) , 'YYYY MON DD' )  as trip_day
, count (*) as nr_points
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
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) 
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) 
, trunc ( l.dt)   
order by trunc ( l.dt ) 
;

! echo .
! read -t 10 -p " ^ list of days in the trip " abc
! echo .

-- points, coordinates of trip
-- optional: draw 1 line per hour, with placemarks at start of hr ?
select t.id
, substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as trpnr 
, substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) as trpnm
-- , count (*) nr_lines
-- , min (dt) earliest, max ( dt) latest 
, to_char ( l.dt, 'YYYY MON DD HH24:MI:SS' ) 
, to_char ( lat, '99.9999' ) || ', ' || to_char ( lon, '99.9999' ) || ', 0 ' 
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

