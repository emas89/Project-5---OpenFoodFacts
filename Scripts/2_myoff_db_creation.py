#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Program which creates the user's database (here named 'myoff_db')

"""

# Import PyMySQL library
import pymysql.cursors

# Connection to 'myoff_db' database
connection = pymysql.connect(
	host = "localhost",
	user = "root",
	password = "")

# Cursor object preparation
cur_object = connection.cursor()


# Database creation: if a previous version is found, it will be erased
sql = "DROP DATABASE IF EXISTS myoff_db; CREATE DATABASE myoff_db CHARACTER SET 'utf8'"
cur_object.execute(sql)

# Grant all privileges to this DB for me (my ID)
sql = "GRANT ALL PRIVILEGES ON myoff_db.* TO 'emanuele'@'localhost'"
cur_object.execute(sql)

# DB creation confirmation
print ("Database created successfully")

connection.commit()
connection.close() # Disconnection from server
