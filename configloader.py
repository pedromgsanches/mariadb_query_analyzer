import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dbhost = str(config['mariadb']['host'])
dbport = config['mariadb']['port']
dbuser = config['mariadb']['user']
dbpwd = config['mariadb']['password']
dbdatabase = config['mariadb']['database']
testruns = config['execution']['testruns']

