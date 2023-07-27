import os
import json
import csv
from datetime import datetime
import requests
import secrets


working_dir = input("Enter the filepath to your working directory. If you do not have one, create a temporary space on your desktop: ")
os.chdir(working_dir)

system = input ('Are you working with dev, dev02 or prod? ')
if system == 'dev':
    baseURL = secrets.dev_baseURL
    user = secrets.dev_adminUser
    password = secrets.dev_adminPassword
    repository = secrets.dev_repository
elif system == 'prod':
    baseURL = secrets.prod_baseURL
    user = secrets.prod_managerUser
    password = secrets.prod_managerPassword
    repository = secrets.prod_repository
elif system == 'dev02':
    baseURL= secrets.dev_02_baseURL
    user = secrets.dev_02_username
    password = secrets.dev_02_password

#Authenticate and set up session in API
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

print("This script will remediate inclusive into single dates when there is a list of known objects.")

csvinput = csv.DictReader(open("inclusiveDateRemediationInput.csv", "r"))

report = []

for row in csvinput:
    AO_uri = row["URI"]
    date_string = row["Dates"].strip("creation: ").replace("T00:00:00+00:00","")
    print(date_string)
    # date_string_single = date_string_inclusive[0]
    # date_object = datetime.strptime(date_string_single, "%Y-%m-%d")
    # # date_string_single_iso = datetime.strftime(date_string_single, "%Y-%m-%d")
    # date_expression = datetime.strftime(date_object, "%Y-%m-%d")
    date_type = "single"

    archival_object_json = requests.get(baseURL + AO_uri, headers=headers).json()
    # print(archival_object_json['lang_materials'])
    # print(archival_object_json)

    date_json = archival_object_json['dates'][0]['begin']
    print(date_json)

    # archival_object_json['dates'][0]["expression"] = date_string
    # archival_object_json["dates"][0]["begin"] = date_string
    # archival_object_json["dates"][0]["date_type"] = date_type
    # try:
    #     for date in archival_object_json['dates']:
    #         keys_to_remove = ['lock_version', 'created_by', 'last_modified_by', 'create_time', 'system_mtime', 'user_mtime', 'end']
    #         for key in keys_to_remove:
    #             date.pop(key)
    # except:
    #     continue
    #
    # updated_archival_object_data = json.dumps(archival_object_json)
    # print(updated_digital_object_data)
    # # print(updated_archival_object_data)
    # try:
    #     archival_object_post = requests.post(baseURL + AO_uri, headers=headers, data=updated_archival_object_data).json()
    #     ao_report = AO_uri + " processed"
    #     print(ao_report)
    #     # report.append(ao_report)
    # except:
    #     # error = print('Yikes! something went wrong with ' + AO_uri)
    #     report.append(error)


# print(report)
