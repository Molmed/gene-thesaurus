# GeneThesaurus v1.0.2

GeneThesaurus is a Python package that translates gene aliases and old gene symbols to the current HGNC standard gene symbols. 

# Installation

You can install GeneThesaurus with:
```
pip install gene-thesaurus
```

# Usage

## translate_genes()

This function takes a list of gene names and returns a list where all possible values are updated to the latest HGNC standard gene symbols.

By default, if a gene name cannot be found, the original gene name is used. If 'nullify_missing' is set to True, these missing genes will be set to None instead.

```
from gene_thesaurus import GeneThesaurus

gt = GeneThesaurus(data_dir='/tmp')
genes = gt.translate_genes(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP', 'MISSING_GENE'])

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C', 'MISSING_GENE']

genes = gt.translate_genes(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP', 'MISSING_GENE'], nullify_missing=True)

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C', None]
```
