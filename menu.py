import calendar as cal
import cdw_data_reader as cdw
import filenames as fn
import os

def get_integer(prompt):
    
    value = input(prompt)
    try: 
        return int(value)
    except ValueError:
        print(f"{value} invalid: Try again.")
        return get_integer(prompt)

def main():
    data = cdw.get_dataframe(fn.CUSTOMER_FILE)

    print(data.head())

        
    # Req-2.1

    # 2.1.1 - Prompt the user for a zip code, provide contextual cues for valid input, and verify it is in the correct format.
    os.system("cls")
    zip_code = input("Enter a 5-digit ZIP code: ")
    while(len(zip_code) != 5 or not zip_code.isnumeric()):
        zip_code = input("Incorrect format. Enter a 5-digit ZIP code: ")

    # 2.1.2- Ask for a month and year,  and provide contextual cues for valid input and verify it is in the correct format.
    os.system("cls")
    print(f"Querying on ZIP code {zip_code}: ")
    months = list(cal.month_name)
    for i,m in enumerate(months):
        if(i > 0): print(i,m)


    month = get_integer("Enter the menu number for the month you want to query: ")
    while month not in range(1,13):
        month = int(input("Invalid month.  Enter the menu number for the month you want to query: "))


    # 2.1.3- Use the provided inputs to query the database and retrieve a list of transactions made by customers in the specified zip code for the given month and year.

    # 2.1.4 - Sort the transactions by day in descending order.

    # Remember: this function should be callable from the main application interface and the output should be screen-reading friendly for the user.
    # 2)    Used to display the number and total values of transactions for a given type.
    # 3)    Used to display the total number and total values of transactions for branches in a given state.

    # 2.2 Customer Details Module

    # Req-2.2

    # Customer Details
    # Functional Requirements 2.2

    # Rubric: - (9%)
    # 1) Used to check the existing account details of a customer.
    # 2) Used to modify the existing account details of a customer.
    # 3) Used to generate a monthly bill for a credit card number for a given month and year. 
    # Hint: What does YOUR monthly credit card bill look like?  What structural components does it have?  Not just a total $ for the month, right?
    # 4) Used to display the transactions made by a customer between two dates. Order by year, month, and day in descending order.

if __name__ == "__main__":
    main()
        