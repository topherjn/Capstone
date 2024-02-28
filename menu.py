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

def make_timeid(year, month, day):
    timeid = str(year) + str(month).rjust(2,'0') + str(day).rjust(2,'0')
    return timeid

# restrict user input to integers
def get_integer(prompt):
    value = input(prompt)
    try:
        return int(value)
    except ValueError:
        print(f"{value} invalid: Try again.")
        return get_integer(prompt)
    
def do_totals_by_category():
    clear_screen()
    category = input("Get counts and totals for transactions in which category? ")
    data_adapter = db.DataAdapter()
    data_adapter.get_transaction_totals_by_category(category)
    data_adapter.close()

def do_totals_by_branch():
    clear_screen()
    data_adapter = db.DataAdapter()
    data_adapter.get_transaction_totals_by_branch()
    data_adapter.close() 

def do_update_customer_details():
    clear_screen()
    ssn = get_integer("Update the details of which customer (SSN)? ")
    data_adapter = db.DataAdapter()
    data_adapter.update_customer_details(ssn)
    data_adapter.close() 

def do_customer_transactions_date_range():
    clear_screen()
    ccn = get_integer("Enter the ssn for the transaction report: ")
    months = list(cal.month_name)
    for i, m in enumerate(months):
        if i > 0:
            print(i, m)

    start_month = get_integer("Enter the menu number for the start month in the range: ")
    while start_month not in range(1, 13):
        start_month = int(input("Invalid month.  Enter the menu number for the start month in the range: "))
    start_year = get_integer(f"{months[start_month]} of which year? ")
    start_day = get_integer(f"What day in {months[start_month]}? ")

    end_month = get_integer("Enter the menu number for the end month in the range: ")
    while end_month not in range(1, 13):
        end_month = int(input("Invalid month.  Enter the menu number for the end month in the range: "))
    end_year = get_integer(f"{months[end_month]} of which year? ")
    end_day = get_integer(f"What day in {months[end_month]}? ")

    start = make_timeid(start_year, start_month, start_day)
    end = make_timeid(end_year, end_month, end_day)

    data_adapter = db.DataAdapter()
    data_adapter.generate_transaction_report(ccn, start, end )
    data_adapter.close()


def do_generate_bill():
    clear_screen()
    ccn = get_integer("Enter the credit card number for which to generate a bill: ")
    year = get_integer("Enter the year of the bill: ")
    months = list(cal.month_name)
    for i, m in enumerate(months):
        if i > 0:
            print(i, m)

    month = get_integer("Which month? ")

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

# get the ssn for customer then call that data adapter
def do_customer_details():
    ssn = get_integer("Enter the social security number for the customer (no dashes): ")
    data_adapter = db.DataAdapter()
    df = data_adapter.get_customer_details(ssn)
    df.show()
    data_adapter.close()

# provides a list of tasks enumerated so user interaction is more efficient
def do_menu():
    
    option = None
    options_dict = {}
    options_dict[1] = "Get a list of transactions by zip, month, and year"
    options_dict[2] = "Get transaction totals by category"
    options_dict[3] = "Get transaction totals by branch"
    options_dict[4] = "Get customer details"
    options_dict[5] = "Update customer details"
    options_dict[6] = "Generate Credit Card Bill"
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
        option = get_integer("Type a number to perform one of the above tasks, 0 to exit: ")

        # launch the chosen option
        match option:
            case 1: do_transactions_query()
            case 2: do_totals_by_category()
            case 3: do_totals_by_branch()
            case 4: do_customer_details()
            case 5: do_update_customer_details()
            case 6: do_generate_bill()
            case 7: do_customer_transactions_date_range()

if __name__ == "__main__":
    do_menu()
