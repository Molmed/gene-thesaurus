from gene_thesaurus import GeneThesaurus
import pytest
import tempfile


data_dir = tempfile.TemporaryDirectory()
data_dir_name = data_dir.name
gt = GeneThesaurus(data_dir=data_dir_name)


def test_update_gene_symbols():
    up_to_date_gene = 'ETV6'
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE',
                  'ZSCAN5CP', up_to_date_gene]
    gt_dict = gt.update_gene_symbols(test_genes)
    assert gt_dict == {'TNFSF2': 'TNF', 'ERBB1': 'EGFR', 'ZSCAN5CP': 'ZSCAN5C'}


def test_translate_genes():
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE',
                  'ZSCAN5CP', 'ETV6']
    gt_dict = gt.translate_genes(test_genes)
    assert gt_dict == {'TNFSF2': 'ENSG00000232810',
                       'ERBB1': 'ENSG00000146648',
                       'ZSCAN5CP': 'ENSG00000204532',
                       'ETV6': 'ENSG00000139083'}


def test_translate_genes_from_ensembl_id():
    test_genes = ['ENSG00000232810',
                  'ENSG00000146648',
                  'ENSG00000204532',
                  'ENSG00000139083',
                  'NOTAREALGENE']
    gt_dict = gt.translate_genes(test_genes, source='ensembl_id',
                                 target='symbol')
    assert gt_dict == {'ENSG00000232810': 'TNF',
                       'ENSG00000146648': 'EGFR',
                       'ENSG00000204532': 'ZSCAN5C',
                       'ENSG00000139083': 'ETV6'}

def test_invalid_gene_translation():
    test_genes = ['ENSG00000232810',
                  'ENSG00000146648',
                  'ENSG00000204532',
                  'ENSG00000139083',
                  'NOTAREALGENE']
    with pytest.raises(ValueError):
        gt.translate_genes(test_genes, source='ensembl_id',
                           target='not_a_valid_target')

    with pytest.raises(ValueError):
        gt.translate_genes(test_genes, source='not_a_valid_source',
                           target='symbol')
