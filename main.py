import mysql
from mysql.connector import Error
from tabulate import tabulate
import sys,os, time, logging
from datetime import datetime
#import configloader
import configparser

# Configure Logging
logging.basicConfig(level = logging.INFO, filename = 'MariadbSQLAnalyzer.log', filemode = 'a')

## Load configurations
try:
    conffile=sys.argv[1]
    sqlpath=sys.argv[2]
except IndexError as e:
    print(f"No arguments given 1-config.ini 2-sqlpath")
    print(f"{e}")
    conffile=None
    sqlpath=None

if conffile:
    print(f"ConfigFile = {conffile}")
    logging.info(f"ConfigFile = {conffile}")    
else:
    conffile='config.ini'
    print(f"ConfigFile = {conffile}")
    logging.info(f"ConfigFile = {conffile}")

if sqlpath:
    print(f"SQL Path = {sqlpath}")
    logging.info(f"SQL Path = {sqlpath}")
else:
    sqlpath='./sql'
    print(f"SQL Path = {sqlpath}")
    logging.info(f"SQL Path = {sqlpath}")


# Config Parser
config = configparser.ConfigParser()
config.read(conffile)

try:
    dbhost = str(config['mariadb']['host'])
    dbport = config['mariadb']['port']
    dbuser = config['mariadb']['user']
    dbpwd = config['mariadb']['password']
    dbdatabase = config['mariadb']['database']
    testruns = config['execution']['testruns']
except KeyError as e:
    logging.error(f"Error loading config file: {e}")
    sys.exit()
    
## Set vars
#dbhost = configloader.dbhost
#dbport = configloader.dbport
#dbuser = configloader.dbuser
#dbpwd = configloader.dbpwd
#dbdatabase = configloader.dbdatabase
#testruns = configloader.testruns

runtimedirs=[sqlpath,f"output/{sqlpath}"]
#directory_path=sqlpath
file_list = os.listdir(sqlpath)
file_list.sort()

## Functions
def calc_values(mylist):
    returnlist=[]
    returnlist.append(sum(mylist) / len(mylist))
    returnlist.append(max(mylist))
    returnlist.append(min(mylist))
    return returnlist

def create_dir(dirname):
    dirpath = os.path.join('./', dirname)
    try:
        os.mkdir(dirpath)         
    except OSError as e:
      if "File exists" not in f"{e}":
        logging.error(f"{e}")


# Start
logging.info(f'Session Start: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

# Create runtime dirs
for dirname in runtimedirs:
    create_dir(dirname) 

## Test DB Connection
try:
    connection = mysql.connector.connect(user=dbuser, password=dbpwd, port=dbport, host=dbhost, database=dbdatabase)
    logging.info("DB Connection is OK")
    connection.close()
except Error as e:
    logging.error(f"{e}")
    sys.exit()

## Start job
for file_name in file_list:
    file_path = os.path.join(sqlpath, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as sqlfile:
            connection = mysql.connector.connect(user=dbuser, password=dbpwd, port=dbport, host=dbhost, database=dbdatabase)
            output = open('./output/'+file_name+'.log', "a")
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
                currrun=int(testruns)
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

                cursor.execute(f"ANALYZE FORMAT=JSON {query}")
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
                #sys.exit()

            output.close()
            cursor.close()
            connection.close()
#connection.close()

logging.info(f'Bye... {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
