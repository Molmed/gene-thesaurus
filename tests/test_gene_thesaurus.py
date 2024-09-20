from gene_thesaurus import GeneThesaurus, HgncException
import pytest
import tempfile
from datetime import datetime
from freezegun import freeze_time


data_dir = tempfile.TemporaryDirectory()
data_dir_name = data_dir.name
gt = GeneThesaurus(data_dir=data_dir_name)


@freeze_time("2023-02-05 12:00:00")
def test_get_last_n_months():
    data_end_time = datetime.now()

    months = GeneThesaurus._get_last_n_months(data_end_time, 6)
    expected_months = ["2023-02", "2023-01", "2022-12",
                       "2022-11", "2022-10", "2022-09"]
    assert months == expected_months

    months = GeneThesaurus._get_last_n_months(data_end_time, 1)
    expected_months = ["2023-02"]
    assert months == expected_months


@freeze_time("2081-04-05 12:00:00")
def test_hgnc_exception():
    with pytest.raises(HgncException):
        GeneThesaurus(data_dir=data_dir_name,
                      data_end_date=datetime.now(),
                      n_attempted_months=2)


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
