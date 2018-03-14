# Open Food Facts Advisor
Open Food Facts Advisor is a program that helps people to eat better.
It is based on public OpenFoodFacts database and recommends the user a healthier food than the initial chosen one.
The advice is made by the comparison between the nutrition scores of the products in the different categories.

# Program Setup
Please note that this program is made for __MySQL only__.
You must have:
- Python **3.x**
- pip
- MySQL
- PyMySQL
- the OFF database in csv extension (download it here https://fr.openfoodfacts.org/data)

# How to use the program
1. Run the first script "*triage.py*" to select the chosen data from OFF database and create your own .csv database file.
2. Run the second script "*myoff_db_creation.py*" to create your database.
3. Run the third script "*tables_creation.py*" to create the database tables. **Note: run this script only once to avoid double data isertions**.
4. Run the fourth script "*data_feeding.py*" to insert data into your database.
5. Run the fifth script "*substitute finder.py*" every time you need a nutritional advice.

- Now you are able to run the main program and get healthier!

# Language
The Open Food Facts Advisor is developed for French citizens. Only the data relating to France and his overseas departments like Martinique, Guadeloupe and similar are in fact have been considered.
