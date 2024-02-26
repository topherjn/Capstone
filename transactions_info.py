import calendar as cal
from os import system, name
import findspark
from build_database import build_database
import dbadapter as db

findspark.init()

# make clear screen platform agnostic-ish
def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# restrict user input to integers
def get_integer(prompt):
    value = input(prompt)
    try:
        return int(value)
    except ValueError:
        print(f"{value} invalid: Try again.")
        return get_integer(prompt)


def transactions_query():
    # Req-2.1

    # 2.1.1 - Prompt the user for a zip code, provide contextual cues for valid input, and verify it is in the
    # correct format.

    # consider getting a list of zip from build_database()
    clear_screen()
    zip_code = input("Enter a 5-digit ZIP code: ")

    while len(zip_code) != 5 or not zip_code.isnumeric():
        zip_code = input("Incorrect format. Enter a 5-digit ZIP code: ")

    # 2.1.2- Ask for a month and year,  and provide contextual cues for valid input and verify it is in the correct
    # format.
        
    # present months menu
    clear_screen()
    print(f"Querying on ZIP code {zip_code}: ")
    months = list(cal.month_name)
    for i, m in enumerate(months):
        if i > 0:
            print(i, m)

    # check user month input
    month = get_integer("Enter the menu number for the month you want to query: ")
    while month not in range(1, 13):
        month = int(input("Invalid month.  Enter the menu number for the month you want to query: "))
        
    # get the year from user
    clear_screen()
    year = get_integer(f"{months[month]} of which year? ")

    # restrict year to 2018
    while year != 2018:
        print("No transaction data for that year.  Try again: ")
        year = get_integer(f"{months[month]} of which year? ")

    # all dataabase operations are performed by this object
    data_adapter = db.DataAdapter()

    data_adapter.get_specified_transactions(zip_code, month, year)

    data_adapter.close()
