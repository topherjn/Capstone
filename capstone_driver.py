from build_database import build_database
from menu import do_menu

'''read in the data and build that MySQL DB from that data first in build_database'''
build_database()

'''do_menu() will control the flow of the user interactions after the database is built'''
do_menu()