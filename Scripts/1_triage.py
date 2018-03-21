#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Program which cleans a csv file from OpenFoodFacts website and put the
selected items into a csv destination file.

"""

# csv module import to manipulate csv format file
import csv
# os module to delete the .csv file if already exists
import os
import sys
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

try:
	os.remove("off_selected.csv")
	print("Previous version deleted.\nCreating new file 'off_selected.csv'...\n")

except:
	print("Creating file 'off_selected'...\n")

# Open the OpenFoodFacts csv file in read mode
f_origin = "fr.openfoodfacts.org.products.csv"
file_read = open(f_origin, newline='', mode='r', encoding='utf8') #utf8 is about character encoding in the file
reader = csv.reader(file_read, delimiter = '\t') # the origin file uses a tab-separation system

# Destination file creation to write in the selected data
f_destination = 'off_selected.csv'
f_write = open(f_destination, newline='', mode='w', encoding='utf8')
writer = csv.writer(f_write, delimiter='\t')

# Insertion of selected data into destination file
for col in reader:
    # Selected columns from the OpenFoodFacts csv file (with its position)
    name = col[7]
    # If the column "product_name" is not empty
    if name:
        brand = col[12]
        # If the column "brands" is not empty
        if brand:
            countries_list = ['France', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',\
             'Polynésie française', 'Saint-Pierre-et-Miquelon', 'Nouvelle-Calédonie',\
             'Union européenne', 'World']
            for cou in countries_list:
                try:
                    countries = col[33]
                    # If the "countries_fr" column contains at least
                    # one of the listed country above
                    if cou == countries:
                        nutrition_grade = col[53]
                        # If the "nutrition_grade_fr" column is not empty
                        if nutrition_grade:
                            categories_list = ['Chips et frites', 'Confitures',\
                            'Crêpes et galettes', 'Desserts au chocolat', 'Gâteaux',\
                            'Pâtes à tartiner', 'Petit-déjeuners', 'Salades composées',\
                            'Sandwichs', 'Tartes']
                            for cat in categories_list:
                                category = col[60]
                                # If the "main_category_fr" column contains at least
                                # one of the listed category above
                                if cat == category:
                                    url = col[1]           # column 'url'
                                    store = col[30]        # column 'stores'
                                    ingredients = col[34]  # column ingredients_text
                                    nutrition_score = col[159]   # column 'nutrition-score-fr_100g'
                                    
                                    # Write selected data into a destination file
                                    writer.writerow([url, name, brand, store, ingredients,\
                                        nutrition_grade, category, nutrition_score])
                except IndexError:
                    pass

print("Destination file created.\n")
file_read.close()  # Close the csv  file