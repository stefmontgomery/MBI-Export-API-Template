import requests
import json
import pandas as pd
import zipfile
import os
from datetime import datetime
import time

# Insert Export API key here
e_api_key = ''

# Insert raw data export ID here
table_id = ''

export_name = 'export_' + datetime.now().strftime('%Y%m%d%H%M')

export_dir = './Exports/'

# Create export file directory
if not os.path.exists(export_dir):
    os.makedirs(export_dir)
    print('Export directory created')

def downloadRawDataExport(e_api_key, table_id, export_name):
    
    ## Create a new copy of the raw data export provided
    h = {'X-RJM-API-Key': e_api_key}
    url = 'https://api.rjmetrics.com/0.1/export/' + table_id + '/copy'
    data = {'name': export_name}

    response = requests.post(url, headers=h, data = data)
    newid = json.loads(response.content)

    print("New Export ID: " + str(newid['export_id']))

    status = ''

    while status not in ('Completed','Error'):
        print( 'Waiting for raw data export to load')
        time.sleep(5)
        info = requests.get('https://api.rjmetrics.com/0.1/export/'
         + str(newid['export_id']) + '/info', headers = h)
        status = json.loads(info.content)['status'] 
    if (status == 'Error'):
        print("Raw data export error")
        raise Exception("Raw data export error!")
    else:
        print("Raw data export loaded")

    # Download the newly created (refreshed) raw data export
    url2 = 'https://api.rjmetrics.com/0.1/export/' + str(newid['export_id'])

    # Download new raw data export
    d = requests.get(url2, headers=h)
    status_code = d.status_code
    if (status_code != 200): 
        raise Exception("Export "+str(newid['export_id'])+" failed with status code "+(str(status_code)))
    
    # Extract CSV data
    zipname = export_dir + export_name+".zip"
    with open(zipname, 'wb') as f:
        f.write(d.content)
    zip = zipfile.ZipFile(zipname)
    zip.extractall(export_dir)

def deleteRawDataExportFiles(export_path):

    zip_file = export_path+".zip"
    ## Delete Zip
    if os.path.isfile(zip_file):
        os.remove(zip_file)
        print("Zip file deleted")
    else:
        print("Error: %s file not found" % zip_file)

    csv_file = export_path+".csv"
    ## Delete CSV
    if os.path.isfile(csv_file):
        os.remove(csv_file)
        print("CSV deleted")
    else:
        print("Error: %s file not found" % csv_file)

downloadRawDataExport(e_api_key, table_id, export_name)

data = pd.read_csv(export_dir + export_name + '.csv', dtype=str)

# Do something with the data here

# Delete the raw data export zip file and CSV
deleteRawDataExportFiles(export_dir + export_name)
