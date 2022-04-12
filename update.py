from psycopg2 import *

con = connect(
    host="ec2-54-157-79-121.compute-1.amazonaws.com",
    database="d8cd5g0t4s4asi",
    user="wcrrtujjtpxjwg",
    password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
)
cur = con.cursor()

cur.execute("select name, mail from data where permission = 'denied';")

records = cur.fetchall()
for record in records:
    print(f"Do you want allow person \n\tname : {record[0]}\n\tmail : {record[1]}\n Response : ", end = "")
    c = input().strip().upper()

    if c == "Y" or c == "YES":
        cur.execute(f"update data set permission = 'allowed' where name = '{record[0]}' and mail = '{record[1]}';")

con.commit()
con.close()

            