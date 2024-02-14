import json

data_folder = 'data'
data_file = 'cdw_sapp_custmer.json'

def get_json_data_as_list(data_file):
        try:
            with open(f"{data_folder}/{data_file}",'r') as fr:
                json_data_list = []
                json_data_item = {}
                data = fr.readline()

                while data:
                    json_data_item['CUSTOMER'] = json.loads(data)
                    json_data_list.append(json_data_item)
                    data = fr.readline()
                    json_data_item = {}
        except Exception as ex:
            print(ex)

        return json_data_list