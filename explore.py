import json


with open('data/cdw_sapp_custmer.json','r') as fr:
    customers = []
    customer = {}
    data = fr.readline()

    while data:
        customer['CUSTOMER'] = json.loads(data)
        customers.append(customer)
        data = fr.readline()
        customer = {}
    lengths = []
    for customer in customers:
       lengths.append(len(str(customer['CUSTOMER']['CUST_ZIP'])))

    print(max(lengths),min(lengths))