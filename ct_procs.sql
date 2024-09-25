
/* ******

ct_procs: creatte procedures, packages to write kml files

todo, mainly add procedures to produce kml::
 - kml_trip-head: placemark, info
 - kml_line_for_day ( trp_id, date )
 -   kml_day_head: placemark, info 
 -   kml_day_end: placemark, info 
 - test resolutions, minute, 10sec, size of files ok ?
****** */

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
  tr_nm         varchar2(100) ;
  tr_start_dt   date ;
  tr_nr_points  number ;
  cr_lf         varchar2(2) := chr(10) ; 
  start_lat     number ;
  start_lon     number ;
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
      -- dbms_output.put_line ( '  kml_trip: ' ||  tr.id       || ', ' || tr.name 
      --                     || ', '           || tr.nr_points || ', started: ' || to_char ( tr.start_dt, 'yyyymmdd hh24miss' ) ); 

      -- need to find starting point from min-dt of trip 

      select l.lat, l.lon
      into  start_lat, start_lon
      from gps_line l
      where rownum < 2 ;

      dbms_output.put_line (
                    '<Placemark> <name>' || tr.name  || '</name>'
        || cr_lf || '  <description> started: ' 
                 || to_char ( tr.start_dt, ' DD MON YYYY HH24:MI' ) 
        || cr_lf || '  </description>'
      ) ; 

      dbms_output.put_line ( 
                    '  <Point>' 
        || cr_lf || '    <coordinates> ' 
                 || to_char ( start_lon, '99.9999' ) || ' , '
                 || to_char ( start_lat, '99.9999' ) || ' , 0 </coordinates> '
        || cr_lf || '  </Point>' 
      ) ; 

      dbms_output.put_line ( '</Placemark>' );

      null ; 

    end loop ; -- for tr loop

end kml_tripstart ; -------------------------
/
show errors


! echo create kml_triplines

create or replace procedure kml_triplines ( tr_id in number ) as 
  tr_nm varchar2(100) ;
  tr_start_dt date ;
  tr_nr_points number ;
begin
  
  -- write line-start
  dbms_output.put_line ( '<Placemark> ' ) ; 
  dbms_output.put_line ( '  <LineString> <coordinates> ' ) ; 

  for line_point in ( select '    '  || to_char ( l.lon, '99.9999' ) 
                          || ', ' || to_char ( l.lat, '99.9999' )  
                          || ', 0.0' as vc_coord 
                        from trip_point tp, gps_line l 
                       where 1=1 
                         and tp.trp_id = tr_id 
                         and tp.gfil_id = l.gfil_id
                         and tp.line_nr = l.line_nr
                         and to_char ( l.dt, 'SS' ) like '00'
                       order by l.dt 
  ) loop

    dbms_output.put_line ( line_point.vc_coord );

  end loop ; -- over lines

  dbms_output.put_line ( '  </coordinates> </LineString> ' );
  dbms_output.put_line ( '</Placemark> ' ) ; 

end kml_triplines ; --------------- 
/
show errors


! echo now for real...

set feedback off
set serveroutput on size unlimited

spool aatest.kml

-- test/call the lot... for trip .. j
declare 
  tr_id         integer ;
  tr_start_dt   date ; 
begin

  kml_head ; 
  kml_tripstart ( 118  ) ; 
  kml_triplines ( 118  ) ; 
  kml_foot ; 
end;
/

spool off

