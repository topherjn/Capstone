import json
import pandas as pd

 

"""
The CDW files are not in a true JSON format. They are more
files with a python dictionary on each line, missing the initial
key for each dictionary.  This module started out as my trying
just to read ZIPs to make sure they're not +9, where I noticed
the lack of compliance to JSON.

This module forces each line into a JSON format and then creates
a list of data items and returns that list to the caller.
"""

# Input: CDW JSON filename
# Returns: List of dictionaries containting JSON objects

data_folder = 'data'
data_file = 'cdw_sapp_custmer.json'

df = pd.read_json(f"{data_folder}/{data_file}", lines=True)

print(df)