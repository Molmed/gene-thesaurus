from pathlib import Path
from datetime import datetime
import os.path
import requests
import json

HGNC_BASE_URL = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/json/'
HGNC_BASE_FILENAME = 'hgnc_complete_set_{month}-01.json'

def get_json_path(data_dir):
    month = datetime.today().strftime('%Y-%m')
    filename = HGNC_BASE_FILENAME.format(month=month)

    path = data_dir + "/" + filename

    if os.path.isfile(path):
        return path

    url = HGNC_BASE_URL + filename
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)

    return path

def get_json_data(data_dir):
    json_path = get_json_path(data_dir)
    
    with open(json_path,'r', encoding='utf8') as f:
        data = json.loads(f.read())

    return data['response']['docs']


def lookup(gene_list, data_dir='/tmp'):
    json = get_json_data(data_dir)

    results = []
    for gene in gene_list:
        for item in json:
            # Currently looks in two different fields: 'prev_symbol' and 'alias_symbol'
            prev_symbol = item.get("prev_symbol", "")
            alias_symbol = item.get("alias_symbol", "")

            if gene.upper() in prev_symbol or gene.upper() in alias_symbol:
                results.append(item.get("symbol"))

    return results
