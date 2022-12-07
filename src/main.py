from sodapy import Socrata
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys
import os
import json


parser = argparse.ArgumentParser(description='Fire Incident Dispatch Data')
parser.add_argument('--page_size', type=int, help='how many rows to get per page', required=True)
parser.add_argument('--num_pages', type=int, help='how many pages to get in total')
args = parser.parse_args(sys.argv[1:])
print(args)


INDEX_NAME=os.environ["INDEX_NAME"]
DATASET_ID=os.environ["DATASET_ID"]
APP_TOKEN=os.environ["APP_TOKEN"]
ES_HOST=os.environ["ES_HOST"]
ES_USERNAME=os.environ["ES_USERNAME"]
ES_PASSWORD=os.environ["ES_PASSWORD"]


if __name__ == '__main__': 
    try:
        resp = requests.put(f"{ES_HOST}/{INDEX_NAME}", auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
            json={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "starfire_incident_id": {"type": "keyword"},
                        "incident_datetime": {"type": "date"},
                        "incident_borough": {"type": "keyword"},
                        "zipcode": {"type": "keyword"},
                        "incident_classification": {"type": "keyword"},
                        "incident_classification_group": {"type": "keyword"},
                        "valid_incident_rspns_time_indc": {"type": "keyword"},
                        "incident_response_seconds_qy": {"type": "float"},
                    }
                },
            }
        )
        resp.raise_for_status()
        print(resp.json())
    except Exception as e:
        print("Index already exists! Skipping")    
    
    client = Socrata("data.cityofnewyork.us", APP_TOKEN, timeout=10000)
    es_rows=[]
    if args.num_pages != args.num_pages:
        data_count = client.get(DATASET_ID, select='Count(*)',where= "starfire_incident_id IS NOT NULL AND incident_datetime IS NOT NULL")
        print("Total number of rows: "+ str(data_count))
        for x in range(int(data_count) / args.page_size):
            rows = client.get(DATASET_ID, limit=args.page_size, offset = (x*args.page_size), where= "starfire_incident_id IS NOT NULL AND incident_datetime IS NOT NULL", order='starfire_incident_id')
            for row in rows:
                try:
                    es_row = {}
                    es_row["starfire_incident_id"] = row["starfire_incident_id"]
                    es_row["incident_datetime"] = row["incident_datetime"]
                    es_row["year"]= int(str(row["incident_datetime"])[:4])
                    es_row["month"]= int(str(row["incident_datetime"])[5:7])
                    es_row["day"]= int(str(row["incident_datetime"])[8:10])
                    es_row["incident_borough"] = row["incident_borough"]
                    es_row["incident_classification"] = row["incident_classification"]
                    es_row["incident_classification_group"] = row["incident_classification_group"]
                    es_row["valid_incident_rspns_time_indc"] = row["valid_incident_rspns_time_indc"]
                    es_row["incident_response_seconds_qy"] = int(row["incident_response_seconds_qy"]) 
                except Exception as e:
                    print (f"Error!: {e}, skipping row: {row}")
                    continue
                es_rows.append(es_row)
                
            bulk_upload_data = ""
            for line in es_rows:
                print(f'Handling row {line["starfire_incident_id"]}')
                action = '{"index": {"_index": "' + INDEX_NAME + '", "_type": "_doc", "_id": "' + line["starfire_incident_id"] + '"}}'
                data = json.dumps(line)
                bulk_upload_data += f"{action}\n"
                bulk_upload_data += f"{data}\n"
            
            try:
                resp = requests.post(f"{ES_HOST}/_bulk",
                            data=bulk_upload_data,auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD), headers = {"Content-Type": "application/x-ndjson"})
                resp.raise_for_status()
                print ('Done')
                        
            except Exception as e:
                print(f"Failed to insert in ES: {e}")
            es_rows = []
    else:
        for x in range(args.num_pages):
            rows = client.get(DATASET_ID, limit=args.page_size, offset = (x*args.page_size), where= "starfire_incident_id IS NOT NULL AND incident_datetime IS NOT NULL", order='starfire_incident_id')
            for row in rows:
                try:
                    es_row = {}
                    es_row["starfire_incident_id"] = row["starfire_incident_id"]
                    es_row["incident_datetime"] = row["incident_datetime"]
                    es_row["year"]= int(str(row["incident_datetime"])[:4])
                    es_row["month"]= int(str(row["incident_datetime"])[5:7])
                    es_row["day"]= int(str(row["incident_datetime"])[8:10])
                    es_row["incident_borough"] = row["incident_borough"]
                    es_row["incident_classification"] = row["incident_classification"]
                    es_row["incident_classification_group"] = row["incident_classification_group"]
                    es_row["valid_incident_rspns_time_indc"] = row["valid_incident_rspns_time_indc"]
                    es_row["incident_response_seconds_qy"] = int(row["incident_response_seconds_qy"]) 
                except Exception as e:
                    print (f"Error!: {e}, skipping row: {row}")
                    continue
                es_rows.append(es_row)
                
            bulk_upload_data = ""
            for line in es_rows:
                print(f'Handling row {line["starfire_incident_id"]}')
                action = '{"index": {"_index": "' + INDEX_NAME + '", "_type": "_doc", "_id": "' + line["starfire_incident_id"] + '"}}'
                data = json.dumps(line)
                bulk_upload_data += f"{action}\n"
                bulk_upload_data += f"{data}\n"
            
            try:
                resp = requests.post(f"{ES_HOST}/_bulk",
                            data=bulk_upload_data,auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD), headers = {"Content-Type": "application/x-ndjson"})
                resp.raise_for_status()
                print ('Done')
                        
            except Exception as e:
                print(f"Failed to insert in ES: {e}")
            es_rows = []
