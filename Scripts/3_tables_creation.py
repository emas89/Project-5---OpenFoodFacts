#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Tables creation in myoff_db database:
columns, primary keys, foreign keys and db engine

"""

# Import PyMySQL library
import pymysql.cursors

# myoff_db database connection with my id and password
connection = pymysql.connect(
    host = "localhost",
    user = "emanuele",
    password = "Senonbestemmio89",
    database = "myoff_db",
    charset = 'utf8', # in MySQL this is the best encoding choice (4 bytes encode)
    autocommit = True) # auto-commit mode for DB connection

# Cursor object preparation
cur_object = connection.cursor()

try:
    # 'Category' table creation
    sql = "CREATE TABLE Category ("\
        "id MEDIUMINT UNSIGNED AUTO_INCREMENT,"\
        "name VARCHAR(100) UNIQUE NOT NULL,"\
        "PRIMARY KEY(id))"\
        "ENGINE = INNODB"
    cur_object.execute(sql)

    # 'Dish' table creation
    sql = "CREATE TABLE Dish ("\
        "id MEDIUMINT UNSIGNED AUTO_INCREMENT,"\
        "category_id MEDIUMINT UNSIGNED NOT NULL,"\
        "name VARCHAR(255) NOT NULL,"\
        "brand VARCHAR(170) NOT NULL,"\
        "ingredients TEXT,"\
        "nutrition_score TINYINT,"\
        "nutrition_grade CHAR(1) NOT NULL,"\
        "url VARCHAR(255) NOT NULL,"\
        "PRIMARY KEY(id))"\
        "ENGINE = INNODB"
    cur_object.execute(sql)

    # 'Store' table creation
    sql = "CREATE TABLE Store ("\
        "id MEDIUMINT UNSIGNED AUTO_INCREMENT,"\
        "name VARCHAR(170),"\
        "PRIMARY KEY(id))"\
        "ENGINE = INNODB"
    cur_object.execute(sql)

    # 'Dish_Store' table creation
    sql = "CREATE TABLE Dish_Store ("\
        "dish_id MEDIUMINT UNSIGNED NOT NULL,"\
        "store_id MEDIUMINT UNSIGNED NOT NULL)"\
        "ENGINE = INNODB"
    cur_object.execute(sql)

    # 'Healthier_Substitute' table creation
    sql = "CREATE TABLE Healthier_Substitute ("\
        "origin_id MEDIUMINT UNSIGNED NOT NULL,"\
        "alternative_id MEDIUMINT UNSIGNED NOT NULL)"\
        "ENGINE = INNODB"
    cur_object.execute(sql)

    # Foreign Keys in 'Dish', 'Dish_Store' and 'Healthier_Substitute' tables
    sql = "ALTER TABLE Dish ADD CONSTRAINT fk_category_id"\
        "FOREIGN KEY (category_id) REFERENCES Category(id);"\
        "ALTER TABLE Dish_Store ADD CONSTRAINT fk_dish_id"\
        "FOREIGN KEY (dish_id) REFERENCES Dish(id);"\
        "ALTER TABLE Dish_Store ADD CONSTRAINT fk_store_id"\
        "FOREIGN KEY (store_id) REFERENCES Store(id);"\
        "ALTER TABLE Healthier_Substitute ADD CONSTRAINT fk_origin_id"\
        "FOREIGN KEY (origin_id) REFERENCES Dish(id);"\
        "ALTER TABLE Healthier_Substitute ADD CONSTRAINT fk_alternative_id"\
        "FOREIGN KEY (alternative_id) REFERENCES Dish(id)"
    cur_object.execute(sql)

except:
    # If the tables have already been created
    print ("\nmyoff_db DB tables already exist.\n")

else:
    # Tables creation confirmation
    print ("\nmyoff_db DB tables created successfully.\n")

finally:
    connection.close() # Disconnection from server
