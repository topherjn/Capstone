# make file names easier
BRANCH_FILE = "cdw_sapp_branch.json"
CREDIT_FILE = "cdw_sapp_credit.json"
CUSTOMER_FILE = "cdw_sapp_custmer.json"
LOAN_FILE = "cdw_sapp_loan.json"

# constants for name strings
DATABASE_NAME = "creditcard_capstone"

# table name constants
BRANCH_TABLE = "CDW_SAPP_BRANCH"
CC_TABLE = "CDW_SAPP_CREDIT_CARD"
CUSTOMER_TABLE = "CDW_SAPP_CUSTOMER"

LOAN_TABLE = "CDW_SAPP_loan_application"

# spark constants
DB_DRIVER = "com.mysql.cj.jdbc.Driver"
DB_URL = "jdbc:mysql://localhost:3306"
JSON_FORMAT = """org.apache.spark.sql.json"""

# REST data file
LOAN_URL = "https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json"

# state postal codes
STATES = [ 'AL','AR','CA','CT','FL','GA','IA','IL','IN','KY','MA','MD','MI',
          'MN','MS','MT','NC','NJ','NY','OH','PA','SC','TX','VA','WA','WI']

STATE_NAMES = {'AL': 'Alabama', 'AR': 'Arkansas', 'CA': 'California', 'CT': 'Connecticut', 'FL': 'Florida', 'GA': 'Georgia', 'IA': 'Iowa', 'IL': 'Illinois', 'IN': 'Indiana', 'KY': 'Kentucky', 'MA': 'Massachusetts', 'MD': 'Maryland', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'NJ': 'New Jersey', 'NY': 'New York', 'OH': 'Ohio', 'PA': 'Pennsylvania', 'SC': 'South Carolina', 'TX': 'Texas', 'VA': 'Virginia', 'WA':'WASHINGTON','WI': 'Wisconsin'
}