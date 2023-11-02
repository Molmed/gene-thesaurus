# GeneThesaurus v1.1.0

GeneThesaurus is a Python package that translates gene aliases and old gene symbols to the current HGNC standard gene symbols. 

# Installation

You can install GeneThesaurus with:
```
pip install gene-thesaurus
```

# Usage

## translate_genes(gene_names, nullify_missing=False)

Parameters:
- gene_names: list
- nullify_missing: bool. By default, if a gene name cannot be found, the original gene name is used. If set to True, these missing genes will be set to None instead.

Returns: a list where all possible values are updated to the latest HGNC standard gene symbols.

## updated_genes(gene_names)

Parameters:
- gene_names: list

Returns: a dict containing all genes that have a newer gene symbol available, in the format {'old_gene_symbol': 'new_gene_symbol'}


## Examples
```
from gene_thesaurus import GeneThesaurus

#########################
### translate_genes() ###
#########################

gt = GeneThesaurus(data_dir='/tmp')
genes = gt.translate_genes(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP', 'MISSING_GENE'])

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C', 'MISSING_GENE']

#####################################################
### translate_genes() with nullify_missing = True ###
#####################################################

genes = gt.translate_genes(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP', 'MISSING_GENE'], nullify_missing=True)

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C', None]

#######################
### updated_genes() ###
#######################

outdated_gene = 'TNFSF2'
up_to_date_gene = 'ETV6'
fake_gene = 'NOTAREALGENE'

updated_genes = gt.updated_genes([outdated_gene, up_to_date_gene, fake_gene])
print(updated_genes)
# {'TNFSF2': 'TNF'}
```

