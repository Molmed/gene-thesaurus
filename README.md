# GeneThesaurus

GeneThesaurus is a Python package that translates gene aliases and old gene symbols to the current HGNC standard gene symbols. 

# Installation

You can install GeneThesaurus with:
```
pip install gene-thesaurus
```

# Example Usage

GeneThesaurus takes a list of gene names and returns a list where all possible values are updated to the latest HGNC standard gene symbols.

By default, if a gene name cannot be found, the original gene name is used. If 'nullify_missing' is set to True, these missing genes will be set to None instead.

## Default example
```
import gene_thesaurus

genes = gene_thesaurus.translate_genes(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP', 'MISSING_GENE'], data_dir='/tmp')

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C', 'MISSING_GENE']
```

## Example with 'nullify_missing'
```
import gene_thesaurus

genes = gene_thesaurus.translate_genes(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP', 'MISSING_GENE'], data_dir='/tmp', nullify_missing=True)

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C', None]
```
