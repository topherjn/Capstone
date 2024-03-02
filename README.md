
# Report 405 - DA Capstone

## Christopher Nicholson - 1st March, 2024

### Summary of Jira Sprints

In the [Jira sprints](./Jira/) we learned how to implement Scrum methodology and use the Jira tool while practicing the concepts we learned in the accompanying module. For instance, we started a sprint, assigned issues to ourselves, wrote SQL scripts to address said issues, and closed the sprint with the appropriate documentation of our work done.

### Core Capstone Components

#### Load Credit Card Database (SQL)

The data for the credit card database were given to us in the form of three JSON files with data on [bank branches](./data/cdw_sapp_branch.json), credit-card [customers](./data/cdw_sapp_custmer.json), and credit-card [transactions](./data/cdw_sapp_credit.json) that we downloaded ahead of time.

In my solution I wrote modules using Python, PySpark, the MySQL connector for Python, and SQL to read the data from these files, transform those data according to specific mapping rules, and write those data to three tables in a locally-running instance of the MySQL RDBMS.

At application start, the module to [build the database](./build_database.py) is called first.  The build_database module will call a [module for reading data](./cdw_data_reader.py) from JSON files to get the data into a suitable format for transforming and writing it to the database, that latter accomplished by using [data adapter class](./dbadapter.py) whose purpose is to perform all database operations, such as creating the database, creating tables, and CRUD operations, including reading data from tables into PySpark dataframe objects.  

#### Application Front-End

Once translated from JSON, transformed, and written to MySQL tables, the data are then available for an end-user to query, which is effected by launching a [menu module](./menu.py) as soon as the build_database module is finished.  This module will offer the user a menu of choices encoded as numbers:

```python
Tasks Menu
[1] - Get a list of transactions by ZIP, month, and year
[2] - Get transaction totals by category
[3] - Get transaction totals by branch
[4] - Get customer details
[5] - Update customer details
[6] - Generate credit card bill
[7] - Get customer transactions in date range
Type a number to perform one of the above tasks, 0 to exit:
```

#### Data Analysis and Visualization

#### Functional Requirements = LOAN Application Dataset

### Conclusion

### Appendix
