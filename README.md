# GeneThesaurus v2.2.0

GeneThesaurus is a Python package that translates between different gene standards using publicly available data from [HGNC](https://www.genenames.org/).

Presently, GeneThesaurus supports translating:
- gene aliases and old gene symbols to the current HGNC standard gene symbols
- gene symbols to ensembl identifiers

Please get in touch (or consider submitting a pull request to this project) if you need translation between other formats.

# Installation

You can install GeneThesaurus with:
```
pip install gene-thesaurus
```

# Example usage
```
from gene_thesaurus import GeneThesaurus
gt = GeneThesaurus(data_dir='/tmp')

outdated_gene = 'TNFSF2'
up_to_date_gene = 'ETV6'
fake_gene = 'NOTAREALGENE'
input = [outdated_gene, up_to_date_gene, fake_gene]

#############################
### update_gene_symbols() ###
#############################

updated_genes = gt.update_gene_symbols(input)
print(updated_genes)
# {'TNFSF2': 'TNF'}

#########################
### translate_genes() ###
#########################

# Valid values for source and target are 'symbol' and 'ensembl_id'.

translated_genes = gt.translate_genes(input, source='symbol', target='ensembl_id')
print(translated_genes)
{'TNFSF2': 'ENSG00000232810', 'ETV6': 'ENSG00000139083'}

```
