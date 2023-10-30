# MariaDB Query Analyzer

## Configurar
1. Colocar ficheiros com 1 query/ficheiro numa pasta (ex: sql)
2. Preencher ficheiro de configuração com base no sample.config.ini

## Executar
1. ./run.sh <config.ini> <./sql>


## Exemplo de resultado em ./output:

###################################################################################################################
Query Start: 24/10/2023 18:34:41
Query_File: query_20231019.sql
Host_Info: ('lxsigdbc01.sys.sibs.pt', '10.5.16-MariaDB-log')
Test_Runs: 10
Avg_Rows: 2 | Max_Rows: 2 | Min_Rows: 2
Avg Exec Time: 0.155062 | Max Exec Time: 1.478147 | Min Exec Time: 0.007109

Execution Plan:
select_type
--------------------------------------------------------------------------------
{
  "query_block": {
    "select_id": 1,
    "r_loops": 1,
    "r_total_time_ms": 6.692736637,
    "table": {
      "table_name": "sr",
      "access_type": "ref",
      "possible_keys": [
        "PRIMARY",
        "FK_SERVICE_REQUEST_X_TERMINAL",
        "IDX_TERMINAL_ID_SERVICE_REQUEST_ID"
      ],
      "key": "FK_SERVICE_REQUEST_X_TERMINAL",
      "key_length": "8",
      "used_key_parts": ["TERMINAL_ID"],
      "ref": ["const"],
      "r_loops": 1,
      "rows": 743,
      "r_rows": 743,
      "r_table_time_ms": 2.218263363,
      "r_other_time_ms": 0.111606306,
      "filtered": 100,
      "r_filtered": 100
    },
(..)
