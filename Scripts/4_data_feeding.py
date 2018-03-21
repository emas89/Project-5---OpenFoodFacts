#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Data insertion in myoff_db database tables. Source file: off_selected.csv

"""

# Import csv module to read the csv file
import csv

# Import PyMySQL library
import pymysql.cursors

# Connection to off_db database with my ID and password
connection = pymysql.connect(
	host = "localhost",
	user = "emanuele",
	password = "Senonbestemmio89",
	database = "myoff_db",
	charset = 'utf8', # in MySQL this is the best encoding choice (4 bytes encode)
	autocommit = True) # auto-commit mode for DB connection

# Cursor object preparation
cur_object = connection.cursor()


""" Category and Dish tables """

# Open selected data from 'off_selected' csv file
file_name = "off_selected.csv"
file_read = open(file_name, newline = '', mode = 'r', encoding = 'utf8')
reader = csv.reader(file_read, delimiter = '\t')
# Data insertion in 'Category' and 'Dish' tables
for col in reader:
	url = col[0]
	name = col[1]
	brand = col[2]
	ingredients = col[4]
	nutrition_grade = col[5]
	category = col[6]
	nutrition_score = col[7]

	# Insert data into 'Category' table and avoid double insertions
	sql = "INSERT IGNORE INTO Category (name) VALUES (%s)"
	cur_object.execute(sql, (category)) #SQL execution

	# Insert data into 'Dish' table
	sql = "INSERT INTO Dish (category_id, name, brand, ingredients, nutrition_score,"\
	"nutrition_grade, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	sql2 = "SELECT id FROM Category WHERE name = %s" # because Dish.category_id = Category.id
	cur_object.execute (sql2, (category))
	result_cat = cur_object.fetchone()
	cur_object.execute(sql, (result_cat, name, brand, ingredients, nutrition_score, nutrition_grade, url))
print("\nTables 'Category' and 'Dish' : data entrance completed.")


""" Store table """

# Open 'off_selected' csv file and read it from the beginning
file_read.seek(0)
# Create a stores list with the different stores in file 'off_selected.csv'
stores_list = []
for col in reader:
	store = col[3]
	store_unit = store.strip().split(',')
	for item in store_unit:
		item = item.strip().capitalize()
		if item and item not in stores_list:
			stores_list.append(item)
stores_list.sort()
# insertion of stores_list in 'Store' table
for label in stores_list:
	sql = "INSERT INTO Store (name) VALUES (%s)"
	cur_object.execute(sql, (label))
print("\nTable 'Store' : data entrance completed.")


""" Dish_Store table """

# Open 'off_selected' csv file and read it from the beginning
file_read.seek(0)
# Data insertion in 'Dish_Store' table
for col in reader:
	store = col[3]
	if store != "":
		store_unit = store.strip().split(',')
		for item in store_unit:
			item = item.strip().capitalize()
			
			# Find the store id
			sql = "SELECT id FROM Store WHERE name = %s"
			cur_object.execute(sql, (item))
			id_store = cur_object.fetchone()
			
			# Find the Dish id by name, brand and url
			sql = "SELECT id FROM Dish WHERE name = %s and brand = %s and url = %s"
			cur_object.execute(sql, (col[1], col[2], col[0]))
			id_dish = cur_object.fetchone()

			# Find the store id for the wanted dish id
			sql = "INSERT INTO Dish_Store (dish_id, store_id) VALUES (%s, %s)"
			cur_object.execute(sql, (id_dish, id_store))
print("\nTable 'Dish_Store' : data entrance completed.")

print ("\nData successfully inserted from 'off_selected.csv' to myoff_db."\
	"\nNow you can run the Open Food facts Advisor program.\n")

file_read.close() # Close 'off_selected.csv' file
connection.close() # Disconnection from server
