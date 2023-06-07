from pathlib import Path
from datetime import datetime
import os.path
import requests
import pandas as pd
import json

HGNC_BASE_URL = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/json/'
HGNC_BASE_FILENAME = 'hgnc_complete_set_{month}-01.json'

def download_json(data_dir):
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

def get_json(date, data_dir):
	json_path = download_json(data_dir)
	
	with open(json_path,'r', encoding='utf8') as f:
		data = json.loads(f.read())

	return data['response']['docs']

def get_df(date, data_dir):
	json = get_json(date, data_dir)
	return pd.json_normalize(json)


def lookup_by_prev_symbol(gene_name, data_dir):
	df = get_df('2023-04-01', data_dir)
	filtered_df = df[df['prev_symbol'].apply(lambda x: isinstance(x, list) and gene_name in x)]
	return filtered_df[['gencc', 'hgnc_id', 'refseq_accession', 'symbol', 'ccds_id', 'omim_id', 'rgd_id', 'merops']]

def lookup(gene_name, data_dir='/tmp'):
	return lookup_by_prev_symbol(gene_name, data_dir)
