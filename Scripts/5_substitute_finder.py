#! /usr/bin/env python3
# -*- coding: utf8 -*-


"""
Open Food Facts Advisor.
Program which finds a healthier food alternative than the one chosen by
the user. The comparison is based on the nutition score: a better dish will
have a higher score than a worse one.
Furthermore, the program indicates where to buy the specified food, if
the information is available in the database.
The user can save his substituted meals in his own database if desired,
or looks at his previous saved meals for a faster choice.

"""

# Original file: OpenFoodFacts database (URL https://world.openfoodfacts.org/data)

from classes import *


def main():
	
	# Welcome message and starting menu
	print("\nHi, welcome to the OpenFood Facts Advisor!\nI hope you will find me useful.\n")
	print('Please choose one of the following options by typing 1 or 2 on your keyboard: \n')
	option = input('1 - You want to find a substitute and healthier aliment.\
    	\n2 - Look at your saved meals.\n')
	while option != '1' and option != '2':
		option = input("You have to type '1' or '2' on your keyboard.\n")

	# Option 1: find a better food alternative
	if option == '1':

		# Display all the categories
		print ('Categories in Database:\n'\
			'(n°, name)\n')
		Mysql_queries.show_category()
		
		# Manage exceptions
		while 1:
			num_cat = input('\nSelect a food category '\
				'(enter a number from 1 to 10): \n')
			try:
				if int(num_cat) in range(1,11):
					break
			except ValueError:
				pass

		# Search for correspondances between user's chosen nb and category id
		cat_nb = List.category_list_id()[int(num_cat)-1]

		# Show to user the meals from the selected category
		print ('\nHere are the meals from selected category:\n'\
			'(n°, name, brand)\n')
		
		# Show up the products of the selected category (20 in every page)
		page_nb = 0
		Mysql_queries.show_dish(cat_nb, page_nb)
		# User interaction with the list
		while 1:
			selected_meal = input("\nSelect your meal by entering his number"\
				" or turn the page by clicking 'n' on your keyboard:\n") # 'n' for 'next'
			min_nb = 1 + 20 * page_nb
			max_nb = min_nb + 20
			try:
				if selected_meal == 'n':
					page_nb += 1
					Mysql_queries.show_dish(cat_nb, page_nb)
				elif int(selected_meal) in range(min_nb, max_nb):
					break
			except ValueError:
				pass
		# Searching for correspondances between user's chosen nb and dish id
		selected_dish = List.dish_list_id(cat_nb)[int(selected_meal)-1]

		# Show up the selected products
		Mysql_queries.show_selected_dish(selected_dish)

		# Suggest a healthier food alternative
		chosen_nb = 0
		# Show up 1 product in every page with its properties
		# User interaction with the list
		Mysql_queries.show_alternative(cat_nb, selected_dish, chosen_nb)
		while 1:
			ok_choice = input ("\nThis product is recommended. Click 'y' to choose it"\
				" or 'o' to see another one\n") # ('y' for 'yes'); ('o' for 'other')
			try:
				if ok_choice == 'o':
					chosen_nb += 1
					Mysql_queries.show_alternative(cat_nb, selected_dish, chosen_nb)
				elif ok_choice == 'y':
					alternative_dish = List.substitute_list_id(cat_nb, selected_dish)\
					[int(chosen_nb)]
					break
			except ValueError:
				pass

		# Show up the store where to buy the suggested meal
		Mysql_queries.show_stores(alternative_dish)

		# Suggestion to save the healthier meal in the 'Healthier_Substitute' table
		db_save = input("\nDo you want to save this meal for later?"\
			" Tap 's' to confirm or any other key to exit.\n")  # ('s' for 'save')
		if db_save == 's':
			Mysql_queries.alternative_save(selected_dish, alternative_dish)
			print("\nMeal saved. You are a little bit healthier now!\nSee you soon. Bye bye!")
		else:
			print("\nSee you soon. Bye bye!")


	# Option 2: find a meal saved in the 'Healthier_Substitute' table
	elif option == '2':
		print('\nHere are the saved meals in your database:\n'\
			'(n°id, name, brand, nutritional level)\n')

		# Display the meals, 10 in every page.
		returned_page = 0
		Mysql_queries.origin_dish_db(returned_page)
		# User interaction with the list
		broken = 1
		while broken:
			id_origin = input("\nSelect a meal by entering his id) "\
				"or type 'n' to see the next page):\n")
			# Check user input
			try:
				if id_origin == 'n':
					returned_page += 1
					Mysql_queries.origin_dish_db(returned_page)
				# Check if the chosen id is on the principal list in the 'Healthier_Substitute' table
				elif id_origin != 'n':
					for j in List.origin_list_id():
						if j == int(id_origin):
							broken = 0
			except ValueError:
				pass

		## Display the selected substitute meal with its properties
		Mysql_queries.alternative_dish_db(id_origin)

		# Goodbye message
		print("\nSee you next time!\n")

# To be standalone
if __name__ == "__main__":
    main()
