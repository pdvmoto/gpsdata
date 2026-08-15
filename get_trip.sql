
! echo now for real...

set feedback off
set verify off
set serveroutput on size unlimited
set linesize 200
set trimspool on

spool aatest.kml

-- test/call the lot... for trip .. j
declare 
  tr_id         integer ;
  tr_start_dt   date ; 
begin

  kml_head ; 
  kml_tripstart ( &&1 ) ; 
  kml_triplines ( &&1 ) ; 
  kml_tripdays  ( &&1 ) ;
  kml_foot ; 
end;
/

spool off

-- show copy command to save file

column cpcmd format A60

set heading off

spool temp_cp.sql

select ' ! cp aatest.kml '
  || substr ( trp_name, instr ( trp_name, '_' )+1, length ( trp_name) ) || '.kml' as cpcmd
from trip t
where t.id = &&1 ;

spool off

set heading on

@temp_cp.sql

! echo now copy the file and run another one


