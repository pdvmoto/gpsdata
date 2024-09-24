
-- ct_procs: creatte procedures, packages to write kml files

! echo create kml_head 

create or replace procedure kml_head as
begin

  dbms_output.put_line (   
'<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
   <Document>
  ' ) ;

end kml_head ;
/
show errors 

! echo create kml_foot

create or replace procedure kml_foot as

begin

  dbms_output.put_line (
' </Document>
</kml>
' ) ; 

end kml_foot;
/
show errors 

! echo create kml_tripstart

create or replace procedure kml_tripstart ( tr_id in number ) as 
  tr_nm varchar2(100) ;
  tr_start_dt date ;
  tr_nr_points number ;
begin
  
  for tr in (
    select    t.id as id
    -- , substr ( trp_name, 1, instr ( trp_name, '_')-1 ) as nr
       , substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) ) as name
       , count (*) nr_points
       , min (dt) start_dt
    from trip t
       , gps_line l
      , trip_point tp
    where 1=1
      and tp.gfil_id = l.gfil_id
      and tp.line_nr = l.line_nr
      and tp.trp_id  = t.id
      and t.id = tr_id 
    group by
      t.id
    , t.trp_name
    , substr ( t.trp_name, instr ( t.trp_name, '_' )+1, length ( t.trp_name) )
    order by 1 ) 
    loop
 
      -- process trip-star: create placemark.
      dbms_output.put_line ( '  kml_trip: ' ||  tr.id       || ', ' || tr.name 
                          || ', '           || tr.nr_points || ', ' || to_char ( tr.start_dt, 'yyyymmdd hh24miss' ) ); 

    end loop ; -- for tr loop

end kml_tripstart ; -------------------------
/
show errors

! echo now for real...

set serveroutput on

spool aatest.kml

-- test/call the lot... for trip .. j
declare 
  tr_id         integer ;
  tr_start_dt   date ; 
begin

  kml_head ; 
  kml_tripstart ( 17  ) ; 
  kml_foot ; 
end;
/

