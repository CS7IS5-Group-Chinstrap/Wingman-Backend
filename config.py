import urllib.parse

DB_USERNAME = 'myuser'
DB_PASSWORD = urllib.parse.quote_plus("MyPassw0rd")
DB_SERVER = 'wingman-server.mysql.database.azure.com'
DB_PORT = '3306'
DB_DATABASE = 'wingman_sc'
USERS_TABLE = 'users'
DB_CONNECT_URL = 'mysql+mysqlconnector://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_SERVER+':'+DB_PORT+'/'+DB_DATABASE
SECRET_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY3OTUyMDg4MCwiaWF0IjoxNjc5NTIwODgwfQ.lHfLnW0gSlZX5Oidv74k96N_AuYtX3lrE-6QF1eqby4'
OPEN_AI_KEY = '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'