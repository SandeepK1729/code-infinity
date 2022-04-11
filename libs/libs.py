from psycopg2 import *
from csv import *
from datetime import datetime

class Record:
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.is_auth_valid = False
        self.login_message = ""

    def validate(self):
        if self.name != "default" and self.pwd != "default":
            con = connect(
                host="ec2-54-157-79-121.compute-1.amazonaws.com",
                database="d8cd5g0t4s4asi",
                user="wcrrtujjtpxjwg",
                password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
            )
            cur = con.cursor()

            # verification of credentials
            cur.execute(f"select name from data where name = '{self.name}' and pwd = '{self.pwd}';")
            if len(cur.fetchall()) != 0:
                self.is_auth_valid = True
            else:
                self.login_message = "Invalid Credentials"
            
            # history
            time_stamp = datetime.now().strftime("%H:%M:%S %d/%m/%y")
            cur.execute(f"insert into history values('{self.name}','{self.pwd}', '{time_stamp}', '{self.is_auth_valid}');")
            
            con.commit()
            con.close()
        
        elif self.name != "default" or self.pwd != "default":
            self.login_message = "Invalid Credentials"

        self.pull()
        return self.login_message


    def push(self):
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
    def pull(self):
        con = connect(
            host="ec2-54-157-79-121.compute-1.amazonaws.com",
            database="d8cd5g0t4s4asi",
            user="wcrrtujjtpxjwg",
            password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
        )
        cur = con.cursor()

        cur.execute("Select * from data;")
        records = cur.fetchall()
        with open("files/data.csv", "w") as file:
            file.write("name,pwd\n")
            for record in records:
                file.write(f"{record[0]},{record[1]}\n")

        cur.execute("Select * from history;")
        
        records = cur.fetchall()
        with open("files/history.csv", "w") as file:
            file.write("name,pwd,time,is_auth_valid\n")
            for record in records:
                # print(record)
                file.write(f"{record[0]},{record[1]},{record[2]},{record[3]}\n")


        con.commit()
        con.close()