from build_database import build_database
from menu import do_menu
import utils as ut

# create the database from the json files, including online
ut.clear_screen()
response = input("Do you wish to rebuild the database? (Y/N) ")

# rebuilding the database every run can be tedious ...
if  len(response) > 0 and response.lower()[0] == "y" :
    build_database()

# launch the menu
do_menu()

