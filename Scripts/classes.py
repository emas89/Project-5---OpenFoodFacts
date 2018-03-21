"""
Classes for 'Open Food Facts Advisor' program

"""

# Import PyMySQL library
import pymysql.cursors

class Connect:
	""" Connection to cleaned database ('myoff_db' database)
		with my access informations """

	CONNECTION = pymysql.connect(
		host = "localhost",
		user = "emanuele",
		password = "Senonbestemmio89",
		database = "myoff_db",
		charset = 'utf8',
		autocommit = True)
	CUR = CONNECTION.cursor()


class List:
	""" Database tables list """

	def category_list_id():
		""" List to collect the ID in 'Category' databse table """
		cat_list = []
		sql = "SELECT id FROM Category"
		Connect.CUR.execute(sql)
		for record in Connect.CUR:
			cat_list.append(record[0])
		return cat_list

	def dish_list_id(cat_nb):
		""" List to collect the ID in 'Dish' databse table """
		dish_list = []
		sql = "SELECT id FROM Dish"
		sql += " WHERE category_id =" +str(cat_nb)
		sql += " ORDER BY name, brand"
		Connect.CUR.execute(sql)
		for record in Connect.CUR:
			dish_list.append(record[0])
		return dish_list

	def substitute_list_id(cat_nb, selected_dish):
		""" List to collect the ID of substitute dishes"""
		substitute_list = []
		sql = "SELECT id FROM Dish"
		sql += " WHERE category_id =" + str(cat_nb)
		sql += " AND nutrition_score < ("
		sql += "SELECT nutrition_score FROM Dish WHERE id =" + str(selected_dish)
		sql += ") ORDER BY nutrition_grade, nutrition_score, name, brand"
		Connect.CUR.execute(sql)
		for record in Connect.CUR:
			substitute_list.append(record[0])
		return substitute_list

	def origin_list_id():
		""" List to collect the ID in 'Healthier_Substitute' databse table """
		list_id_origin = []
		sql = "SELECT DISTINCT origin_id FROM Healthier_Substitute"
		Connect.CUR.execute(sql)
		for record in Connect.CUR:
			list_id_origin.append(record[0])
		return list_id_origin


class Mysql_queries:
	""" MySQL queries to search and save data """

	def show_category():
		""" Method to search all categories names """
		sql = "SELECT name FROM Category"
		Outcome.category(sql)

	def show_dish(cat_nb, page_nb):
		""" Method to search the name and brand of all dishes in a selected category """
		sql = "SELECT name, brand FROM Dish WHERE category_id=" + str(cat_nb)
		sql += " ORDER BY name, brand"
		sql += " LIMIT " + str(page_nb*15) + ", 15" # to limit the number of returned rows
		Outcome.dish(sql, page_nb)

	def show_selected_dish(selected_dish):
		""" Method to search the name and nutrition grade of a selected meal """
		sql = "SELECT name, nutrition_grade FROM Dish WHERE id =" + str(selected_dish)
		Outcome.selection(sql)

	def show_alternative (cat_nb, selected_dish, chosen_nb):
		""" Method to search an healthier alternative in a selected category """
		sql = "SELECT name, brand, ingredients, nutrition_score, nutrition_grade, url"
		sql += " FROM Dish WHERE category_id =" + str(cat_nb)
		sql += " AND nutrition_score < ("
		sql += "SELECT nutrition_score FROM Dish WHERE id =" + str(selected_dish)
		sql += ") ORDER BY nutrition_grade, nutrition_score, name, brand"
		sql += " LIMIT " + str(chosen_nb) + ", 1"
		Outcome.alternative(sql)

	def show_stores(alternative_dish):
		""" Method to search the sores where the user can buy the healthier food """
		sql = "SELECT s.name"
		sql += " FROM Store AS s"
		sql += " INNER JOIN Dish_Store AS ds"
		sql += " ON s.id = ds.store_id"
		sql += " WHERE ds.dish_id =" + str(alternative_dish)
		Outcome.store(sql)

	def alternative_save(selected_dish, alternative_dish):
		""" Method to save the alternative meal in 'Healthier_Substitute' table """
		sql = "INSERT INTO Healthier_Substitute (origin_id, alternative_id) VALUES (%s, %s)"
		Connect.CUR.execute(sql,(selected_dish, alternative_dish))

	def origin_dish_db(returned_page):
		""" Method to search the name, brand and nutrition grade in 'Healthier_Substitute' table """
		sql = "SELECT d.id, d.name, d.brand, d.nutrition_grade"
		sql += " FROM Dish AS d"
		sql += " INNER JOIN Healthier_Substitute as h"
		sql += " ON d.id = h.origin_id"
		sql += " ORDER BY name, brand, nutrition_grade"
		sql += " LIMIT " + str(returned_page * 10) + ", 10"
		Outcome.origin_db(sql)

	def alternative_dish_db(id_origin):
		""" Method to search for an alternative meal starting from a selected one """
		sql = "SELECT d.name, d.brand, d.nutrition_grade"
		sql += " FROM Dish as d"
		sql += " INNER JOIN Healthier_Substitute AS h"
		sql += " ON d.id = h.alternative_id"
		sql += " WHERE h.origin_id =" + str(id_origin)
		Outcome.alternative_db(sql)


class Outcome:
	""" MySQL queries outcomes """

	def category(sql):
		""" Method to list and enumerate the categories """
		Connect.CUR.execute(sql)
		i = 1
		for record in Connect.CUR:
			print (i, record[0])
			i += 1

	def dish(sql, page_nb):
		""" Method to list and enumerate the dishes """
		Connect.CUR.execute(sql)
		i = 1 + page_nb * 15
		for record in Connect.CUR:
			print (i, record)
			i += 1

	def selection(sql):
		""" Method to show the nutrition grade of the dish """
		Connect.CUR.execute(sql)
		print ("Chosen dish: ")
		for record in Connect.CUR:
			print(" Nutrition grade: ".join(record))

	def alternative(sql):
		""" Method to show the alternative meal and his attributes """
		Connect.CUR.execute(sql)
		print("\nRecommended alternative: \n"\
			"(name, brand, ingredients, nutri-score, nutri-grade, url)\n")
		for record in Connect.CUR:
			print(record)

	def store(sql):
		""" Method to show the alternative food's stores if present in the database """
		Connect.CUR.execute(sql)
		print("\nYou can find this dish in this/these market(s): \n")
		for record in Connect.CUR:
			print ("".join(record))

	def origin_db(sql):
		""" Method to show all selected dishes in the 'Healthier_Substitute' table """
		Connect.CUR.execute(sql)
		for record in Connect.CUR:
			print (record)

	def alternative_db(sql):
		""" MEthod to show the selected alternative and their attributes """
		Connect.CUR.execute(sql)
		print ("\nYou have chosen this healthier alternative:\n"\
			"(name, brand, nutri-grade)\n")
		for record in Connect.CUR:
			print (record)