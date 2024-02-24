from transactions_info import transactions_query

def do_menu():

    # ask user the task he wishes to perform
    # call the code for the task requested

    
    # 2.1.3- Use the provided inputs to query the database and retrieve a list of transactions made by customers in
    # the specified zip code for the given month and year. 2.1.4 - Sort the transactions by day in descending order.
    # z,m,y = data_adapter.get_specified_transactions(zip_code,month,year)

    '''done'''
    transactions_query()

    # Remember: this function should be callable from the main application interface and the output should be
    # screen-reading friendly for the user. 
    # 2)    Used to display the number and total values of transactions for a
    # given type.
    """This can be done post query"""
    # 3)    Used to display the total number and total values of transactions for branches in a given state.
    """This can be done post query"""

    # 2.2 Customer Details Module

    # Req-2.2

    # Customer Details
   

    


if __name__ == "__main__":
    do_menu()
