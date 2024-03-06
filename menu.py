import calendar as cal
from os import system, name
import findspark
from build_database import build_database
import dbadapter as db
import constants as const
import utils as ut

findspark.init()

# make clear screen platform agnostic-ish
def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# get the category from the user then call the function
def do_totals_by_category():
    clear_screen()
    category = input("Get counts and totals for transactions in which category? ")
    data_adapter = db.DataAdapter()
    data_adapter.get_transaction_totals_by_category(category)
    data_adapter.close()

# no use input needed here
def do_totals_by_state():
    clear_screen()
    # get the desired state
    state = input("Get transactions totals for which state (postal code)? ")

    # check user error
    while state.upper() not in const.STATES:
        print(f"No branches in {state}.")
        state = input("Get transactions totals for which state? ")

    data_adapter = db.DataAdapter()
    data_adapter.get_transaction_totals_by_state(state)
    data_adapter.close() 

# just need the ssn for this
def do_update_customer_details():
    clear_screen()
    ssn = ut.get_integer("Update the details of which customer (SSN)? ")
    data_adapter = db.DataAdapter()
    data_adapter.update_customer_details(ssn)
    data_adapter.close() 

# get the cc#, start time and end time and show the transactions
# in that range
def do_customer_transactions_date_range():
    clear_screen()
    ccn = ut.get_integer("Enter the ssn for the transaction report: ")
    months = list(cal.month_name)
    for i, m in enumerate(months):
        if i > 0:
            print(i, m)

    # this could probably be modularized but not bothering because of the limited uses
    start_month = ut.get_integer("Enter the menu number for the start month in the range: ")

    while start_month not in range(1, 13):
        start_month = int(ut.get_integer("Invalid month.  Enter the menu number for the start month in the range: "))

    start_year = ut.get_integer(f"{months[start_month]} of which year? ")
    start_day = ut.get_integer(f"What day in {months[start_month]}? ")

    end_month = ut.get_integer("Enter the menu number for the end month in the range: ")
    
    while end_month not in range(1, 13):
        end_month = int(input("Invalid month.  Enter the menu number for the end month in the range: "))
    end_year = ut.get_integer(f"{months[end_month]} of which year? ")
    end_day = ut.get_integer(f"What day in {months[end_month]}? ")

    start = ut.make_timeid(start_year, start_month, start_day)
    end = ut.make_timeid(end_year, end_month, end_day)

    data_adapter = db.DataAdapter()
    if start <= end:
        data_adapter.generate_transaction_report(ccn, start, end )
    else:
        print("Aborting: start date after end date")
    data_adapter.close()

# get the cc# year and month 
# and this will show customer name, transactions with categories,
# and total for the month
def do_generate_bill():
    clear_screen()
    ccn = ut.get_integer("Enter the credit card number for which to generate a bill: ")
    year = ut.get_integer("Enter the year of the bill: ")
    months = list(cal.month_name)
    for i, m in enumerate(months):
        if i > 0:
            print(i, m)

    month = ut.get_integer("Which month? ")

    data_adapter = db.DataAdapter()
    data_adapter.generate_cc_bill(str(ccn),month,year)
    data_adapter.close()

def do_transactions_query():
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
    month = ut.get_integer("Enter the menu number for the month you want to query: ")
    while month not in range(1, 13):
        month = int(input("Invalid month.  Enter the menu number for the month you want to query: "))
        
    # get the year from user
    clear_screen()
    year = ut.get_integer(f"{months[month]} of which year? ")

    # restrict year to 2018
    while year != 2018:
        print("No transaction data for that year.  Try again: ")
        year = ut.get_integer(f"{months[month]} of which year? ")

    # all dataabase operations are performed by this object
    data_adapter = db.DataAdapter()

    data_adapter.get_specified_transactions(zip_code, month, year)

    data_adapter.close()

# get the ssn for customer then call that data adapter
def do_customer_details():
    ssn = ut.get_integer("Enter the social security number for the customer (no dashes): ")
    data_adapter = db.DataAdapter()
    df = data_adapter.get_customer_details(ssn)
    
    # show only customers who exist
    if not df.rdd.isEmpty():
        df.show(n=df.count(),truncate=False)
    else:
        print(f"Customer {ssn} does not exist.")

    data_adapter.close()

# provides a list of tasks enumerated so user interaction is more efficient
def do_menu():
    
    option = None
    options_dict = {}
    options_dict[1] = "Get a list of transactions by ZIP, month, and year"
    options_dict[2] = "Get transaction totals by category"
    options_dict[3] = "Get transaction totals for branches in a state"
    options_dict[4] = "Get customer details"
    options_dict[5] = "Update customer details"
    options_dict[6] = "Generate credit card bill"
    options_dict[7] = "Get customer transactions in date range"
    
    # this flag is just to make press enter idempotent
    flag = False
    while not option==0:
        # don't prompt to hit enter on first run
        if not flag:
            flag = True
        else:
            input("Type Enter to continue: ")
        clear_screen()

        # use the dict created above to present the options
        print("Tasks Menu")
        for key, value in options_dict.items():
            print(f'[{key}] - {str(value)}')
        
        # get the option from the user
        option = ut.get_integer("Type a number to perform one of the above tasks, 0 to exit: ")

        # launch the chosen option
        match option:
            case 1: do_transactions_query()
            case 2: do_totals_by_category()
            case 3: do_totals_by_state()
            case 4: do_customer_details()
            case 5: do_update_customer_details()
            case 6: do_generate_bill()
            case 7: do_customer_transactions_date_range()
            case 0: print("Exiting ...")
            case _: print("Not an option.")

if __name__ == "__main__":
    do_menu()
