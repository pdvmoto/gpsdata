
/* 
ct_gprmc : table to receive GPS data of type GPRMC

note: load-only table, no pk, not much checks yet.

*/

-- drop table gprmc; 
create table gprmc ( 
  log_header varchar2(6)    -- check '$GPRMC'
, utc_hhmmss date           -- add any yyymmmdd, check not null.
, pos_status varchar2(1)    -- check : A=ok or V=invalid
, lat        number         -- latitide, DDmm.mmmmmm, converting to DD.mmm?
, lat_dir    varchar2(1)    -- direction, check: N or S
, lon        number         -- longitude, DDmm.mmmm.
, lon_dir    varchar2(1)    -- direction, check E or W
, speed_kn   number         -- grondspeed, Knots
, track_true number         -- direction, degrees, check [ 0, 360 >.
, dt         date           -- dd/mm/yy, check validity, store with time=0
, mag_var    number         -- check >= 0
, var_dir    varchar2(1)    -- check E=subtract from true W=add to true
, mode_ind   varchar2(1)    -- check: Auto, Diff, Est, Manual, Notvalid
, checksum   varchar2(3)    -- check: *nn, how to check?
)
;

create sequence position_log_seq; 

create table position_log ( 
  id     number not null        -- which route, 
, dt         date   not null        -- measurment, to 1 sec precision
, lat        number         -- latitude, degrees, decimal, S=negative
, lat_dir    varchar2(1)    -- direction, check: N or S
, lon        number         -- longitude, degrees, decimal, W=Negative
, lon_dir    varchar2(1)    -- direction, check E or W
, pos_status varchar2(1)    -- check : A=ok or V=invalid
, speed_kn   number         -- grondspeed, Knots
, track_true number         -- direction, degrees, check [ 0, 360 >.
, mag_var    number         -- check >= 0
, var_dir    varchar2(1)    -- check E=subtract from true W=add to true
, mode_ind   varchar2(1)    -- check: Auto, Diff, Est, Manual, Notvalid
, checksum   varchar2(3)    -- check: *nn, how to check?
)
;

create unique index position_log_pk on position_log ( id, dt ) ; 


/**** 
more complete datamodel:

for loading:
 - gps_file : id + name + path + earliest data
 - gps_line : key= (gfil_id, glin_nr) + all data + raw_line

for trip logs:
 - trip: id + name + startdate  +...
 - trip_point :  trip_id, gfil_id, glin_nr, + any derived relevant data.
 - trip_stop :   trip_id, stop_dt, opintal: link to  file_line, + any relevant data, notes
 - trip_point_map :  subset of trip_points, reduce data for kml/kmz/gpx files, faster drawing.
            note: can also flag trip_point as "mappable".

background: 
Raw data remains in file_lines. 
Trip is mainly componsed by linking to lines. 
and lines implicitly have an ordering in line_nr and timestamps.
for mapping: not all points are needed. 
if points are close, speed=same,  heading=same.. removed points in between..

***/

/**/

drop sequence trip_seq; 
drop sequence gps_file_seq;

drop table trip_point ;
drop table trip_stop ;
drop table trip ; 

drop table gps_file ;
drop table gps_line ;

create sequence trip_seq;
create sequence gps_file_seq;

create table gps_file ( 
  id            number          not null
, fname         varchar2(128)   not null
, fpath         varchar2(128) 
, dt_loaded     date            not null    -- date the file was read/loaded.
, dt_earliest   date                        -- earliest data in the file (dependent..)
) ; 

alter table gps_file add constraint gps_file_pk primary key ( id ) using index ; 

create table gps_line (
  gfil_id       number          not null 
, line_nr       number          not null 
, dt         date           -- date from line-info, if null chk file earliest/ or dt
, lat        number         -- latitude, degrees, decimal, S=negative
, lat_dir    varchar2(1)    -- direction, check: N or S
, lon        number         -- longitude, degrees, decimal, W=Negative
, lon_dir    varchar2(1)    -- direction, check E or W
, pos_status varchar2(1)    -- check : A=ok or V=invalid
, speed_kn   number         -- grondspeed, Knots
, track_true number         -- direction, degrees, check [ 0, 360 >.
, mag_var    number         -- check >= 0
, var_dir    varchar2(1)    -- check E=subtract from true W=add to true
, mode_ind   varchar2(1)    -- check: Auto, Diff, Est, Manual, Notvalid
, chksum     varchar2(2)    -- checksum, see GGRMC spec, bitwise and, I think
) ; 

-- notes: consider timestamp for more precision ?
-- notes: if no dt, then assume order-by file-earliest + linenr
-- notes: consider not-null on several fields to always have valid lon/lat
-- notes: consider check+range on several fields.

alter table gps_line add constraint gps_line_pk primary key ( gfil_id, line_nr ) using index ; 
alter table gps_line add constraint gps_line_trp_fk foreign key ( gfil_id ) references trip ( id ) ; 


create table trip (
  id        number not null
, trp_name  varchar2 ( 255) 
, start_dt  date 
);

alter table trip add constraint trip_pk primary key ( id ) using index ;

create index trip_name on trip ( trp_name ) ;


-- consider this an IOT + 2ndary index on trp_id
create table trip_point ( 
  gfil_id       number not null
, line_nr       number not null
, trp_id        number not null
) ;

alter table trip_point add constraint trip_point_pk     primary key ( gfil_id, line_nr, trp_id ) using index ; 

create index trip_point_trp_idx on trip_point ( trp_id, gfil_id, line_nr ) ;

alter table trip_point add constraint trip_point_fk_trp foreign key ( trp_id ) references trip ( id ) ;
alter table trip_point add constraint trip_point_fk_gln foreign key ( gfil_id, line_nr ) references gps_line ( gfil_id, line_nr ) ;

