
# Report 405 - DA Capstone

## Christopher Nicholson - 1st March, 2024

### Summary of Jira Sprints

In the [Jira sprints](./Jira/) we learned how to implement Scrum methodology and use the Jira tool while practicing the concepts we learned in the accompanying module. For instance, we started a sprint, assigned issues to ourselves, wrote SQL scripts to address said issues, and closed the sprint with the appropriate documentation of our work done.

### Core Capstone Components

1. Load Credit Card Database (SQL)

The data for the credit card database were given to us in the form of three JSON files with data on [bank branches](./data/cdw_sapp_branch.json), credit-card [customers](./data/cdw_sapp_custmer.json), and credit-card [transactions](./data/cdw_sapp_credit.json) that we downloaded ahead of time.

In my solution I wrote modules using Python, PySpark, the MySQL connector for Python, and SQL to read the data from these files, transform those data according to specific mapping rules, and write those data to three tables in a locally-running instance of the MySQL RDBMS.

At application start, the module to [build the database](./build_database.py) is called first.  This module calls an instance of a data adapter class I wrote whose purpose is to perform all database operations.  

1. Application Front-End
1. Data Analysis and Visualization
1. Functional Requirements = LOAN Application Dataset

### Conclusion

### Appendix
