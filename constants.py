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

LOAN_URL = "https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json"

JSON_FORMAT = """org.apache.spark.sql.json"""
