# GeneThesaurus

GeneThesaurus is a Python package that translates gene aliases and old gene symbols to the current HGNC standard gene symbols. 

# Example Usage
```
import gene_thesaurus

genes = gene_thesaurus.lookup(['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP'], data_dir='/tmp')

print(genes)
# ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']
```
