from psycopg2 import *
from csv import *
from datetime import datetime
from random import choices
from string import ascii_letters, digits
import smtplib
from os import environ




class Record:
    def __init__(self, username, pwd, name = "", mail = "", ):
        self.username = username
        self.pwd = pwd
        self.is_auth_valid = False
        self.is_auth_default = True
        self.login_message = ""
        self.register_message = ""
        self.name = name
        self.mail = mail
        self.is_exist = False

        self.from_mail = "code.infinity.nocto@gmail.com"
        self.from_mail_pwd = "codeinfinity140422"
        # self.from_mail = environ['CODE_INFINITY_MAIL_ID']
        # self.from_mail_pwd = environ['CODE_INFINITY_PWD']
    def validate(self):
        if self.username != "default" and self.pwd != "default":
            
            self.is_auth_default = False
            con = self.connect_to_db()
            cur = con.cursor()

            # verification of credentials
            cur.execute(f"select username from data where username = '{self.username}' and pwd = '{self.pwd}';")
            if len(cur.fetchall()) != 0:
                # self.push()
                self.is_exist = True
                cur.execute(f"select username from data where username = '{self.username}' and pwd = '{self.pwd}' and permission = 'allowed';")
                
                if len(cur.fetchall()) != 0:
                    self.is_auth_valid = True
                    self.register_message = "Account Credentials already exist, try to login"
                else:
                    self.register_message = "Account Credentials already exist, but Account not activated yet"
                    self.login_message = "Your Account not activated yet"
                    
            else:
                self.is_exist = False
                self.login_message = "Invalid Credentials"
            
            # history
            time_stamp = datetime.now().strftime("%H:%M:%S %d/%m/%y")
            cur.execute(f"insert into history values('{self.username}','{self.pwd}', '{time_stamp}', '{self.is_auth_valid}');")
            
            con.commit()
            con.close()
        
        elif self.username != "default" or self.pwd != "default":
            self.login_message = "Invalid Credentials"

        self.pull()
        if self.is_auth_default:
            self.login_message = ""

        return self.is_auth_valid
    def push(self):
        con = self.connect_to_db()
        cur = con.cursor()

        cur.execute("delete from data;")

        with open("files/data.csv") as file:
            records = DictReader(file)
            for record in records:
                cur.execute("insert into data values('{name}', '{mail}', '{username}', '{pwd}', '{permission}');".format(name = record["name"], mail = record["mail"], username = record["username"], pwd = record["pwd"], permission = record["permission"]))

        con.commit()
        con.close()
    def pull(self):
        con = self.connect_to_db()
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
        con = self.connect_to_db()
        cur = con.cursor()

        # history
        time_stamp = datetime.now().strftime("%H:%M:%S %d/%m/%y")
        cur.execute(f"insert into data values('{self.name}', '{self.mail}', '{self.username}', '{self.pwd}', 'denied');")
        cur.execute(f"insert into history values('{self.username}','{self.pwd}', '{time_stamp}', 'ttr');")

    

        # verification
        cur.execute("select code from verifier;")

        codes = cur.fetchall()
        # random hashcode generator 
        code = ""
        for i in range(8):
            code += "".join(choices(ascii_letters + digits))

        while code in codes:
            code = ""
            for i in range(8):
                code += "".join(choices(ascii_letters + digits))
            
        cur.execute(f"insert into verifier values ( '{self.name}', '{self.mail}', '{code}');") 
        self.verification_mail(self.name, self.mail, code)

        self.pull()
        self.is_auth_default = True

        con.commit()
        con.close()
    def verification_mail(self, name, to_mail, code):
        to_mail = [to_mail]
        mail_subject = "Code Infinity Account Activation"
        mail_body = f"""
Hi {name},

We just need to verify your email address before you can access Code Infinity Portal.

Verify your email address, { "https://code-infinity.herokuapp.com/account-verification?code=" + code }

Best regards, The Code Infinity team
        """
        email_text = """\
From: %s
To: %s
Subject: %s

%s
        """ % (self.from_mail, to_mail, mail_subject, mail_body)
        
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)       # route
            smtp_server.ehlo()                                          # connecting
            smtp_server.login(self.from_mail , self.from_mail_pwd)      # login
            smtp_server.sendmail(self.from_mail , to_mail, email_text)  # sending
            smtp_server.close()                                         # close
            print ("Email sent successfully!")
        except Exception as ex:
            print ("Something went wrong….",ex)
    @staticmethod
    def connect_to_db():
        """
        return connect(
            host = environ['HEROKU_POSTGRESQL_HOST'], 
            database = environ['HEROKU_POSTGRESQL_DATABASE'],
            user = environ['HEROKU_POSTGRESQL_USER'],
            password = environ['HEROKU_POSTGRESQL_PWD']
        )"""
        return connect(
            host = "ec2-54-157-79-121.compute-1.amazonaws.com", 
            database = "d8cd5g0t4s4asi",
            user = "wcrrtujjtpxjwg",
            password = "21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
        )
    @staticmethod
    def verify_mail(code):
        is_valid = True
        con = Record.connect_to_db()
        cur = con.cursor()

        cur.execute(f"select name, mail from verifier where code = '{code}';")

        data = cur.fetchall()
        if len(data) == 0:
            con.close()
            return False
        
        data = data[0]
        
        name, mail = data[0], data[1]
        cur.execute(f"update data set permission = 'allowed' where name = '{name}' and mail = '{mail}';")
        
        con.commit()
        con.close()
        return True
    """ for automatic login route
    def relay(self, now = False):
        if datetime.now().strftime("%H") != "23" and not now:
            return ""
    
        con = connect(
            host="ec2-54-157-79-121.compute-1.amazonaws.com",
            database="d8cd5g0t4s4asi",
            user="wcrrtujjtpxjwg",
            password="21dcc6fdae16a8b1243226940b05afb76613dc66c3b073ab78a1f206f4a39597"
        )
        cur = con.cursor()

        self.push()
        cur.execute(f"delete from data where permission = 'denied'")
        self.pull()

        con.commit()"""
        