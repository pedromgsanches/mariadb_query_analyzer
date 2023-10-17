import mysql
from mysql.connector import Error
from tabulate import tabulate
import os, time, logging
from datetime import datetime
import connection_info

## Set vars
dbhost = connection_info.dbhost
dbport = connection_info.dbport
dbuser = connection_info.dbuser
dbpwd = connection_info.dbpwd
dbdatabase = connection_info.dbdatabase
testruns = connection_info.testruns
directory_path='./sql'
file_list = os.listdir(directory_path)

logging.basicConfig(level = logging.INFO, filename = 'mariadb_query_analyzer.log', filemode = 'w')


## Functions
def calc_values(mylist):
    returnlist=[]
    returnlist.append(sum(mylist) / len(mylist))
    returnlist.append(max(mylist))
    returnlist.append(min(mylist))
    return returnlist



# Start
logging.info(f'Session DateTime: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    

## Test DB Connection
try:
    connection = mysql.connector.connect(user=dbuser, password=dbpwd, port=dbport,
            host=dbhost,
            database=dbdatabase)
    logging.info("DB Connection is OK")
except Error as e:
    logging.error(f"{e}")

## Start job
for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as sqlfile:
            output = open(file_name+'_log.log', "a")

            # Start
            output.write("#############################################################################################################################\n")
            output.write("Query Start: "+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"\n")
            logging.info(f'Query Start: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

            # Query file Info
            file_contents = sqlfile.read()
            output.write(f"Query_File: {file_name}\n")
            logging.info(f"Query_File: {file_name}")

            query = file_contents

            # Host Info
            iquery = 'select @@hostname,version()'
            icursor = connection.cursor()
            icursor.execute(iquery)
            result = icursor.fetchall() 
            for row in result: 
                output.write('Host_Info: '+str(row)+"\n")
            output.write('Test_Runs: '+str(testruns)+"\n")

            # Execute Query
            cursor = connection.cursor()
            execlist=[]
            rocolist=[]
            try:
                currrun=testruns
                while currrun>0:
                    logging.info(f"-- Current Run: {currrun}")
                    currrun=currrun-1
                    start_time = time.time()
                    cursor.execute(query)
                    end_time = time.time()
                    execlist.append(end_time - start_time)
                    rocolist.append(len(cursor.fetchall()))

                rowinfo = calc_values(rocolist)
                output.write(f"Avg_Rows: {rowinfo[0]:.0f} | Max_Rows: {rowinfo[1]} | Min_Rows: {rowinfo[2]} \n")
                execinfo = calc_values(execlist)
                output.write(f"Avg Exec Time: {execinfo[0]:.6f} | Max Exec Time: {execinfo[1]:.6f} | Min Exec Time: {execinfo[2]:.6f} \n")

                cursor.execute(f"EXPLAIN {query}")
                execution_plan = cursor.fetchall()


                rowcount = len(cursor.fetchall())
                query_time = end_time - start_time

                output.write("\nExecution Plan:\n")
                col_list=('select_type', 'table', 'type', 'possible_keys', 'key', 'ken_len', 'ref', 'rows', 'Extra')

                output.write(tabulate(execution_plan, headers=col_list, tablefmt="simple"))
                output.write("\n \n")

            except Error as e:
                output.write(f"Error: {e}\n")
                logging.error(f"{e}")


            output.close()
            cursor.close()

logging.info(f'Bye... {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

            

connection.close()