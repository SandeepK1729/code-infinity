from psycopg2 import *
from csv import *

def push():
    con = connect(
        host="ec2-54-157-79-121.compute-1.amazonaws.com",
        database="d8cd5g0t4s4asi",
        user="wcrrtujjtpxjwg",
        password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
    )
    cur = con.cursor()

    with open("data.csv") as file:
        records = DictReader(file)
        for record in records:
            cur.execute("insert into data values('{name}', '{pwd}');".format(name = record["name"], pwd = record["pwd"]))

    con.commit()
    con.close()
