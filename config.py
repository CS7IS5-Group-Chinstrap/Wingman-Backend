import urllib.parse

DB_USERNAME = 'myuser'
DB_PASSWORD = urllib.parse.quote_plus("Wingman@123")
DB_SERVER = 'wingman-server.mysql.database.azure.com'
DB_PORT = '3306'
DB_DATABASE = 'wingman_sc'
USERS_TABLE = 'users'
DB_CONNECT_URL = 'mysql+mysqlconnector://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_SERVER+':'+DB_PORT+'/'+DB_DATABASE