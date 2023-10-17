# MariaDB Query Analyzer

## Config
1. Place SQL files in 'sql' folder
2. Connection info in config.ini

## Execute script
1. Load venv ./Scripts/activate*
2. Run: python ./main.py

## Compile
1. compile.bat
2. files in ./dist

## Required files
config.ini
sql/*
output/


## Output files like:

#############################################################################################################################
Query Start: 17/10/2023 15:48:09
Query_File: query1.sql
Host_Info: ('PSAN-OMX', '10.6.7-MariaDB')
Test_Runs: 5
Avg_Rows: 898480 | Max_Rows: 898480 | Min_Rows: 898480
Avg Exec Time: 2.527729 | Max Exec Time: 2.559655 | Min Exec Time: 2.451204

Execution Plan:
    select_type    table    type    possible_keys     key                 ken_len  ref              rows  Extra
--  -------------  -------  ------  ----------------  ----------------  ---------  -------------  ------  --------------------------------------------
 1  SIMPLE         o        ALL     ix_order_id                                                   238917  Using where; Using temporary; Using filesort
 1  SIMPLE         c        ref     ix_customer_id    ix_customer_id            4  tpcc.o.o_c_id      38
 1  SIMPLE         ol       ref     ix_orderline_oid  ix_orderline_oid          4  tpcc.o.o_id       388