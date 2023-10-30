from pathlib import Path
from datetime import datetime
import os.path
import requests
import json

HGNC_BASE_URL = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/json/'
HGNC_BASE_FILENAME = 'hgnc_complete_set_{month}-01.json'
GENE_THESAURUS_BASE_FILENAME='gene_thesaurus_{month}-01.json'

def get_month():
    return datetime.today().strftime('%Y-%m')

def get_hgnc_json_path(data_dir):
    filename = HGNC_BASE_FILENAME.format(month=get_month())
    path = data_dir + "/" + filename

    if os.path.isfile(path):
        return path

    url = HGNC_BASE_URL + filename
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)

    return path

def get_hgnc_json_data(data_dir):
    json_path = get_hgnc_json_path(data_dir)
    
    with open(json_path,'r', encoding='utf8') as f:
        data = json.loads(f.read())

    return data['response']['docs']

def get_gene_thesaurus_dict(data_dir):
    filename = GENE_THESAURUS_BASE_FILENAME.format(month=get_month())
    json_path = data_dir + "/" + filename

    # If dict already exists, return it
    if os.path.isfile(json_path):
        with open(json_path,'r', encoding='utf8') as f:
            data = json.loads(f.read())
            return data
        
    # Otherwise, construct it from the hgnc data and then return it
    hgnc_json = get_hgnc_json_data(data_dir)

    # Convert to simple dict, where each 'symbol', 'prev_symbol' and 'alias_symbol' all map to 'symbol'
    gene_dict = {}
    for item in hgnc_json:
        # The current gene name
        symbol = item.get("symbol")
        gene_dict[symbol] = symbol

        # Optionally available older synonyms
        prev_symbols = item.get("prev_symbol", [])
        for sym in prev_symbols:
            gene_dict[sym] = symbol
        alias_symbols = item.get("alias_symbol", [])
        for sym in alias_symbols:
            gene_dict[sym] = symbol

    # Save the gene dict
    with open(json_path, 'w') as file:
        json.dump(gene_dict, file)

    return gene_dict

def translate_genes(gene_list, data_dir='/tmp', nullify_missing=False):
    gene_thesaurus_dict = get_gene_thesaurus_dict(data_dir)

    results = []
    for gene in gene_list:
        try:
            symbol = gene_thesaurus_dict[gene]
        except:
            print("Could not find {}".format(gene))
            if nullify_missing:
                symbol = None
            else:
                symbol = gene
        results.append(symbol)

    return results
