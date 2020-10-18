
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

