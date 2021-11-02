import mysql.connector as sql
import sys, random

if len(sys.argv) > 1:
    username = sys.argv[1]
    password = sys.argv[2]
else:
    username = input("username: ")
    password = input("password: ")
client = sql.connect(
    username = username,
    password = password
)
cursor = client.cursor()



def dbcreate():
    '''creates new database'''
    dbname = "medmanage" + str(int(random.random()*1000000))
    cursor.execute("show databases")
    if dbname in cursor.fetchall():
        dbcreate()
    cursor.execute(f"create database {dbname}")
    client.commit()
    with open("configuration.py") as conf:
        content = conf.readlines()
    for i in range(len(content)):
        if content[i].startswith("username"):
            content[i] = f"username = '{username}'\n"
        if content[i].startswith("password"):
            content[i] = f"password = '{password}'\n"
        if content[i].startswith("database"):
            content[i] = f"database = '{dbname}'\n"
    with open("configuration.py", "w") as conf:
        conf.writelines(content)
    cursor.execute(f"use {dbname}")

def createstock():
    '''creates stock table'''
    command = "create table stock (batch varchar(50), medname varchar(100), quantity int(12), cp decimal(8, 2), dealer varchar(100), buydate date, mfgdate date, expdate date)"
    cursor.execute(command)
    client.commit()

def createsold():
    '''creates sold table'''
    command = "create table sold (batch varchar(50), medname varchar(100), quantity int(12), cp decimal(8, 2), sp decimal(8, 2), dealer varchar(100), customer varchar(100), buydate date, selldate date, mfgdate date, expdate date)"
    cursor.execute(command)
    client.commit()

def createdumped():
    '''creates table dumped'''
    command = "create table dumped (batch varchar(50), medname varchar(100), quantity int(12), cp decimal(8, 2), dealer varchar(100), buydate date, mfgdate date, expdate date)"
    cursor.execute(command)
    client.commit()

def createsell():
    ''' table sell'''
    command = "create table sell (batch varchar(50) primary key, medname varchar(100), quantity int(12), sp decimal(8, 2), customer varchar(100), selldate date)"
    cursor.execute(command)
    client.commit()


if __name__ == "__main__":
    dbcreate()
    createstock()
    createsold()
    createdumped()
    createsell()
