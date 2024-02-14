import json

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

def get_json_data_as_list(data_file):
        json_data_list = []

        # make the json dict keys correspond
        # to which file
        base_key = str(data_file)

        try:
            # should open any known cdw
            with open(f"{data_folder}/{data_file}",'r') as fr:
                
                # read the first line
                data = fr.readline()

                # read in all the lines i.e. all the data items
                while data:
                    json_data_item = json.loads(data)
                    json_data_list.append(json_data_item)
                    data = fr.readline()
        except Exception as ex:
            print(ex)

        # send the list of data items back to caller
        return json_data_list