# 1) Create a function that accomplishes the following tasks:
# 1. 2.1.1 - Prompt the user for a zip code, provide contextual cues for
# valid input, and verify it is in the correct format.
# 2. 2.1.2- Ask for a month and year, and provide contextual cues for
# valid input and verify it is in the correct format.
# 3. 2.1.3- Use the provided inputs to query the database and retrieve
# a list of transactions made by customers in the specified zip code
# for the given month and year.
# 4. 2.1.4 - Sort the transactions by day in descending order.
# Remember: this function should be callable from the main application
# interface and the output should be screen-reading friendly for the user.
# 2) Used to display the number and total values of transactions for a
# given type.
'''SELECT transaction_type, count(*),sum(transaction_value)
from cdw_sapp_credit_card
group by transaction_type;'''
# 3) Used to display the total number and total values of transactions for
# branches in a given state.
'''select b.BRANCH_STATE, count(cc.TRANSACTION_ID), sum(cc.TRANSACTION_VALUE)
from cdw_sapp_credit_card cc inner join cdw_sapp_branch b on cc.BRANCH_CODE = b.BRANCH_CODE
group by b.branch_state
order by b.BRANCH_STATE;'''
