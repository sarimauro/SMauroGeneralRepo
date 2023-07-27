import os
import json
import csv
import requests
import secrets

print("This script works from a list of known objects with single dates and removes any erroneous timestamps associated with the date fields. This script is designed to work from a work order plug in report, but will also work with any CSV input with AO URIs and Dates. Name your input file timestampRemediationInput.csv")

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

# csv = csv.reader(open("timestampRemediationInput.csv", "r"))


input = csv.DictReader(open("timestampRemediationInput.csv"))

for row in input:
    # print(row)
    uri = row["URI"]
    date = row["Dates"].replace("creation: ","").replace("T00:00:00+00:00","")
    print(date)

    ao_json = requests.get(baseURL + uri, headers=headers).json()
    # ao_dates = ao_json["dates"]
    ao_json["dates"][0]["expression"] = date
    ao_json["dates"][0]["begin"] = date
    ao_json["dates"][0]["date_type"] = "single"

    for date in ao_json['dates']:
        keys_to_remove = ['lock_version', 'created_by', 'last_modified_by', 'create_time', 'system_mtime', 'user_mtime']
        for key in keys_to_remove:
            date.pop(key)

    updated_archival_object_data = json.dumps(ao_json)
    # print(updated_archival_object_data)
    # print(updated_archival_object_data)

    archival_object_post = requests.post(baseURL + uri, headers=headers, data=updated_archival_object_data).json()
    ao_report = uri + " processed"
    print(ao_report)

print("Done!")
        # report.append(ao_report)
