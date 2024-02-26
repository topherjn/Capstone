    # 3) Used to generate a monthly bill for a credit card number for a given month
    # and year. Hint: What does YOUR monthly credit card bill look like?  What structural components does it have?
    # Not just a total $ for the month, right? 

def generate_cc_bill(ccn, month, year):
    pass
    ''' 
    select TIMEID, TRANSACTION_TYPE, TRANSACTION_VALUE
    from cdw_sapp_credit_card
    where CREDIT_CARD_NO = '4210653349028689' and timeid like "201802%"
    '''

    '''
    select sum(TRANSACTION_VALUE)
    from cdw_sapp_credit_card
    where CREDIT_CARD_NO = '4210653349028689' and timeid like "201802%"
    '''

    if __name__ == "__main__":
        pass