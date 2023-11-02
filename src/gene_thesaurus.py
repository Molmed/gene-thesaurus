from datetime import datetime, timedelta
import os.path
import requests
import json
import logging


class HgncException(Exception):
    def __init__(self, message="Could not obtain HGNC data."):
        self.message = message
        super().__init__(self.message)


class GeneThesaurus:
    _HGNC_BASE_URL = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/json/'  # noqa: E501
    _HGNC_BASE_FILENAME = 'hgnc_complete_set_{month}-01.json'
    _GENE_THESAURUS_BASE_FILENAME = 'gene_thesaurus_{month}-01.json'

    def __init__(self,
                 data_dir='/tmp',
                 data_end_date=datetime.now(),
                 n_attempted_months=6):

        # Logging
        self.logger = logging.getLogger(__class__.__name__)

        # Public
        self.gene_dict = None

        # Private
        self.__data_dir = data_dir
        self.__data_end_date = data_end_date
        self.__n_attempted_months = n_attempted_months
        self.__hgnc_data_month = None
        self.__hgnc_json_path = None
        self.__hgnc_data = None

        # Try getting HGNC data for the past n months
        months = self._get_last_n_months(self.__data_end_date,
                                         self.__n_attempted_months)

        for month in months:
            filename = self._HGNC_BASE_FILENAME.format(month=month)
            path = self.__data_dir + "/" + filename
            found = False

            if os.path.isfile(path):
                found = True
            else:
                url = self._HGNC_BASE_URL + filename
                r = requests.get(url)
                if r.status_code == 200:
                    found = True
                    with open(path, 'wb') as f:
                        f.write(r.content)

            if found:
                self.__hgnc_data_month = month
                self.__hgnc_json_path = path
                break

        # If we have maxed out number of attempts, throw exception
        if not self.__hgnc_data_month or not self.__hgnc_json_path:
            raise HgncException(
                f"Could not retrieve HGNC data from {self._HGNC_BASE_URL}")

        # Load the HGNC JSON data
        with open(self.__hgnc_json_path, 'r', encoding='utf8') as f:
            data = json.loads(f.read())
            self.__hgnc_data = data['response']['docs']

        # Prepare the gene dict, where each 'symbol', 'prev_symbol'
        # and 'alias_symbol' all map to 'symbol'
        dict_filename = self._GENE_THESAURUS_BASE_FILENAME.format(
            month=self.__hgnc_data_month)
        dict_json_path = self.__data_dir + "/" + dict_filename

        # Does it already exist?
        if os.path.isfile(dict_json_path):
            with open(dict_json_path, 'r', encoding='utf8') as f:
                self.gene_dict = json.loads(f.read())
        else:
            self.gene_dict = {}
            for item in self.__hgnc_data:
                # The current gene name
                symbol = item.get("symbol")
                self.gene_dict[symbol] = symbol

                # Optionally available older synonyms
                prev_symbols = item.get("prev_symbol", [])
                for sym in prev_symbols:
                    self.gene_dict[sym] = symbol
                alias_symbols = item.get("alias_symbol", [])
                for sym in alias_symbols:
                    self.gene_dict[sym] = symbol

            # Save the gene dict
            with open(dict_json_path, 'w') as file:
                json.dump(self.gene_dict, file)

    @staticmethod
    def _get_last_n_months(data_end_date, n_months):
        return [(data_end_date - timedelta(days=30 * i)).
                strftime('%Y-%m') for i in range(n_months)]

    def translate_genes(self, gene_list, nullify_missing=False):
        results = []
        for gene in gene_list:
            try:
                symbol = self.gene_dict[gene]
            except KeyError:
                self.logger.info("Could not find {}".format(gene))
                if nullify_missing:
                    symbol = None
                else:
                    symbol = gene
            results.append(symbol)

        return results

    def updated_genes(self, gene_list):
        return {key: self.gene_dict[key] for key in gene_list
                if key in self.gene_dict and key != self.gene_dict[key]}
