from pathlib import Path
import os.path
import requests
import pandas as pd
import json

HGNC_BASE_URL = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/json/'
HGNC_BASE_FILENAME = 'hgnc_complete_set_{date}.json'
DATA_PATH = str(Path(__file__).parent.parent.absolute()) + '/data/'
FALLBACK_DB_DATE = '2023-05-01'

def download_json(date):
	filename = HGNC_BASE_FILENAME.format(date=date)
	path = DATA_PATH + filename

	if os.path.isfile(path):
		return path

	url = HGNC_BASE_URL + filename
	r = requests.get(url)
	with open(path, 'wb') as f:
		f.write(r.content)

	return path

def get_json(date):
	json_path = download_json('2023-04-01', encoding='utf8')
	
	with open(json_path,'r') as f:
		data = json.loads(f.read())

	return data['response']['docs']

def get_df(date):
	json = get_json(date)
	return pd.json_normalize(json)


def lookup_by_prev_symbol(gene_name):
	df = get_df('2023-04-01')
	#print(df.columns)
	#print(df['gtrnadb'])
	filtered_df = df[df['prev_symbol'].apply(lambda x: isinstance(x, list) and gene_name in x)]
	return filtered_df[['gencc', 'hgnc_id', 'refseq_accession', 'symbol', 'ccds_id', 'omim_id', 'rgd_id', 'merops']]

def lookup(gene_name):
	return lookup_by_prev_symbol(gene_name)

print(lookup('ZSCAN5CP'))
