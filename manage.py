from psycopg2 import *
from libs.libs import Record
from flask import session

con = Record.connect_to_db()
cur = con.cursor()

cur.execute("select * from data;")

records = cur.fetchall()
for record in records:
    print(f"Do you want stay person \n\tname : {record[0]}\n\tmail : {record[1]}\n\tusername : {record[2]}\n\tpwd : {record[3]}\n\tpermission : {record[4]}\n Response : ", end = "")
    c = input().strip().upper()

    if c == "Y" or c == "YES":
        cur.execute(f"update data set permission = 'allowed' where name = '{record[0]}' and mail = '{record[1]}';")
        
    elif c == "N" or c == "NO":
        cur.execute(f"delete from data where name = '{record[0]}' and mail = '{record[1]}';")
        # if session.get("name"):
        #    session["name"] = None
if len(records) == 0:
    print("no accounts for now")

Record("", "").pull()
con.commit()
con.close()

            