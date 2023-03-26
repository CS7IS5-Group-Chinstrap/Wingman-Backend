
import json
import pandas as pd
from datetime import datetime as dt
import random
import mysql.connector

cnx = mysql.connector.connect(user='myuser', password='Wingman@123',
                              host='wingman-server.mysql.database.azure.com', port = '3306',
                              database='wingman_sc')
cursor = cnx.cursor()



df = pd.read_csv (r'okcupid_profiles.csv')
df.insert(0, 'id', range(0, 0 + len(df)))
print(len(df))
df = df.dropna()
print(len(df))
df.drop(
        [
           "status",
           "body_type",
           "drugs",
           "height",
           "income",
           "last_online",
           "offspring",
           "smokes"
        ],
        axis=1,
        inplace=True,
    )
m_names = ["Liam","Noah","Oliver","Elijah","James","William","Benjamin","Lucas", "Henry","Theodore"]
f_names = ["Olivia","Emma","Charlotte","Amelia","Ava","Sophia","Isabella","Mia","Evelyn","Harper"]

names = []



# for index, row in df.iterrows():  
#      if(row.sex == 'm'):
#           names.append(random.choice(m_names))
#      elif( row.sex == 'f'):
#           names.append(random.choice(f_names))     
#      else:
#           names.append(random.choice(f_names.append(m_names)))

# df["name"] = names

cursor.execute("TRUNCATE TABLE wingman_sc.users")

for index, row in df.head(500).iterrows():  
     if(len(row.essay0)>10000 or len(row.essay1)>5000):
          continue
     if(row.sex == 'm'):
          name = random.choice(m_names)
     else:
          name = random.choice(f_names)
     insert_stmt = "INSERT INTO wingman_sc.users (id, age, sex, orientation, diet, drinks, education, ethnicity, job, location, pets, religion, sign, speaks, essay0, essay1, essay2, essay3, essay4, essay5, essay6, essay7, essay8, essay9, firstname) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"   
     data = ( row.id, row.age, row.sex, row.orientation, row.diet, row.drinks, row.education, row.ethnicity, row.job, row.location, row.pets, row.religion, row.sign, row.speaks, row.essay0, row.essay1, row.essay2, row.essay3, row.essay4, row.essay5, row.essay6, row.essay7, row.essay8, row.essay9, name)
     cursor.execute(insert_stmt, data)

print(df.head())

cnx.commit()
cursor.close()



