from unicodedata import name
from psycopg2 import *
from csv import *
from datetime import datetime

class Record:
    def __init__(self, username, pwd, name = "", mail = "", ):
        self.username = username
        self.pwd = pwd
        self.is_auth_valid = False
        self.is_auth_default = True
        self.login_message = ""
        self.name = name
        self.mail = mail
        self.is_exist = True
    def validate(self):
        if self.username != "default" and self.pwd != "default":
            self.is_auth_default = False
            con = connect(
                host="ec2-54-157-79-121.compute-1.amazonaws.com",
                database="d8cd5g0t4s4asi",
                user="wcrrtujjtpxjwg",
                password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
            )
            cur = con.cursor()

            # verification of credentials
            cur.execute(f"select username from data where username = '{self.username}' and pwd = '{self.pwd}';")
            if len(cur.fetchall()) != 0:
                cur.execute(f"select username from data where username = '{self.name}' and pwd = '{self.pwd}' and permission = 'allowed';")
                if len(cur.fetchall()) != 0:
                    self.is_auth_valid = True
                    self.is_exist = True
                else:
                    self.login_message = "Your Account not activated yet"
            else:
                self.login_message = "Invalid Credentials"
            
            # history
            time_stamp = datetime.now().strftime("%H:%M:%S %d/%m/%y")
            cur.execute(f"insert into history values('{self.username}','{self.pwd}', '{time_stamp}', '{self.is_auth_valid}');")
            
            con.commit()
            con.close()
        
        elif self.username != "default" or self.pwd != "default":
            print(self.username, self.pwd)
            self.login_message = "Invalid Credentials"

        self.pull()
        if self.is_auth_default:
            self.login_message = ""

        return self.is_auth_valid
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
                cur.execute("insert into data values('{name}', '{mail}', '{username}', '{pwd}', '{permission}');".format(name = record["name"], mail = record["mail"], username = record["username"], pwd = record["pwd"], permission = record["permission"]))

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
            file.write("name,mail,username,pwd,permission\n")
            for record in records:
                file.write(f"{record[0]},{record[1]},{record[2]},{record[3]},{record[4]}\n")

        cur.execute("Select * from history;")

        records = cur.fetchall()
        with open("files/history.csv", "w") as file:
            file.write("name,pwd,time,is_auth_valid\n")
            for record in records:
                # print(record)
                file.write(f"{record[0]},{record[1]},{record[2]},{record[3]}\n")


        con.commit()
        con.close()
    def register_new(self):
        con = connect(
            host="ec2-54-157-79-121.compute-1.amazonaws.com",
            database="d8cd5g0t4s4asi",
            user="wcrrtujjtpxjwg",
            password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
        )
        cur = con.cursor()

        cur.execute(f"insert into data values('{self.name}', '{self.mail}', '{self.username}', '{self.pwd}', 'denied');")
        self.is_auth_default = True

        con.commit()
        con.close()
        