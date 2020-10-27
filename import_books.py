import requests
import os
import json


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as infile:
        result = json.load(infile)

    return result


src_directory = "book_data"
headers = {"Content-Type": "application/json"}

for jsonfile in os.listdir(src_directory):
    file_path = os.path.join(src_directory, jsonfile)
    data = read_file(file_path)

    r = requests.post('http://localhost:8000/api/migration/', headers=headers, json=data)
    print("{} {}".format(file_path, r.status_code))
