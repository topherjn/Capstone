import calendar as cal
import cdw_data_parser as cdw

data = cdw.get_json_data_as_list('cdw_sapp_custmer.json')


customer_zips = [item['CUST_ZIP'] for item in data]

customer_zip = input("Give me a ZIP: ")
if customer_zip not in customer_zips:
    print("Invalid zip")

# Req-2.1

# 2.1.1 - Prompt the user for a zip code, provide contextual cues for valid input, and verify it is in the correct format.

    
# 5 or 9?


# 2.1.2- Ask for a month and year,  and provide contextual cues for valid input and verify it is in the correct format.

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

