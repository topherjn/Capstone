from build_database import build_database
from menu import do_menu

# create the database from the json files, including online
response = input("Do you wish to rebuild the database? (Y/N) ")

if response.lower()[0] == "y":
    build_database()

# launch the menu
do_menu()
