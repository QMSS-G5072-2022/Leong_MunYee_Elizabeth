#import sys
#sys.path.insert(0, '../src/')
from springerclient_ml4837 import ResultsAnalysis
from springerclient_ml4837 import check_parameters

# did not work:
# from springerclient_ml4837 import springerclient_ml4837
# from src.springerclient_ml4837 import springerclient_ml4837
# https://stackoverflow.com/questions/74215098/python-no-module-named-src
# from .src.springerclient_ml4837 import springerclient_ml4837
# from ..src.springerclient_ml4837 import springerclient_ml4837; "attempted relative import with no known parent package"
# https://realpython.com/absolute-vs-relative-python-imports/#absolute-imports


import pytest
import requests.exceptions
import pandas as pd

df_list = [['Article',
  'doi:10.1186/gb-spotlight-20001229-02',
  'en',
  'http://dx.doi.org/10.1186/gb-spotlight-20001229-02',
  'And the winner is...',
  'Wells, William',
  'Genome Biology',
  'false',
  '10.1186/gb-spotlight-20001229-02',
  'BioMed Central',
  '2000-12-29',
  'Journal',
  '1474-760X',
  '1',
  '1',
  'OriginalPaper, Research news',
  '1',
  '2',
  '13059',
  '©2000 BioMed Central Ltd',
  '',
  'Life Sciences, Animal Genetics and Genomics, Human Genetics, Plant Genetics and Genomics, Microbial Genetics and Genomics, Bioinformatics, Evolutionary Biology'],
 ['Article',
  'doi:10.1186/gb-2000-2-1-interactions0001',
  'en',
  'http://dx.doi.org/10.1186/gb-2000-2-1-interactions0001',
  'Genome sequences and great expectations',
  'Iliopoulos, Ioannis; Tsoka, Sophia; Andrade, Miguel A; Janssen, Paul; Audit, Benjamin; Tramontano, Anna; Valencia, Alfonso; Leroy, Christophe; Sander, Chris; Ouzounis, Christos A',
  'Genome Biology',
  'false',
  '10.1186/gb-2000-2-1-interactions0001',
  'BioMed Central',
  '2000-12-29',
  'Journal',
  '1474-760X',
  '2',
  '1',
  'OriginalPaper, Open letter',
  '1',
  '3',
  '13059',
  '©2000 GenomeBiology.com',
  'To assess how automatic function assignment will contribute to genome annotation in the next five years, we have performed an analysis of 31 available genome sequences. An emerging pattern is that function can be predicted for almost two-thirds of the 73,500 genes that were analyzed. Despite progress in computational biology, there will always be a great need for large-scale experimental determination of protein function.',
  'Life Sciences, Animal Genetics and Genomics, Human Genetics, Plant Genetics and Genomics, Microbial Genetics and Genomics, Bioinformatics, Evolutionary Biology'],
 ['Article',
  'doi:10.1186/rr33',
  'en',
  'http://dx.doi.org/10.1186/rr33',
  'Matrix metalloproteinases in lung biology',
  'Parks, William C; Shapiro, Steven D',
  'Respiratory Research',
  'true',
  '10.1186/rr33',
  'BioMed Central',
  '2000-12-29',
  'Journal',
  '1465-993X',
  '2',
  '1',
  'OriginalPaper, Review',
  '1',
  '10',
  '12931',
  '©2001 BioMed Central Ltd',
  'Despite much information on their catalytic properties and gene regulation, we actually know very little of what matrix metalloproteinases (MMPs) do in tissues. The catalytic activity of these enzymes has been implicated to function in normal lung biology by participating in branching morphogenesis, homeostasis, and repair, among other events. Overexpression of MMPs, however, has also been blamed for much of the tissue destruction associated with lung inflammation and disease. Beyond their role in the turnover and degradation of extracellular matrix proteins, MMPs also process, activate, and deactivate a variety of soluble factors, and seldom is it readily apparent by presence alone if a specific proteinase in an inflammatory setting is contributing to a reparative or disease process. An important goal of MMP research will be to identify the actual substrates upon which specific enzymes act. This information, in turn, will lead to a clearer understanding of how these extracellular proteinases function in lung development, repair, and disease.',
  'Medicine & Public Health, Pneumology/Respiratory System'],
 ['Article',
  'doi:10.1186/rr37',
  'en',
  'http://dx.doi.org/10.1186/rr37',
  'Risk factors for hospitalization among adults with asthma: the influence of sociodemographic factors and asthma severity',
  'Eisner, Mark D; Katz, Patricia P; Yelin, Edward H; Shiboski, Stephen C; Blanc, Paul D',
  'Respiratory Research',
  'true',
  '10.1186/rr37',
  'BioMed Central',
  '2000-12-29',
  'Journal',
  '1465-993X',
  '2',
  '1',
  'OriginalPaper, Research',
  '1',
  '8',
  '12931',
  '©2001 Eisner et al, licensee BioMed Central Ltd on behalf of the copyright holder',
  'Background The morbidity and mortality from asthma have markedly increased since the late 1970s. The hospitalization rate, an important marker of asthma severity, remains substantial. Methods In adults with health care access, we prospectively studied 242 with asthma, aged 18–50 years, recruited from a random sample of allergy and pulmonary physician practices in Northern California to identify risk factors for subsequent hospitalization. Results Thirty-nine subjects (16%) reported hospitalization for asthma during the 18-month follow-up period. On controlling for asthma severity in multiple logistic regression analysis, non-white race (odds ratio [OR], 3.1; 95% confidence interval [CI], 1.1–8.8) and lower income (OR, 1.1 per $10,000 decrement; 95% CI, 0.9–1.3) were associated with a higher risk of asthma hospitalization. The severity-of-asthma score (OR, 3.4 per 5 points; 95%, CI 1.7–6.8) and recent asthma hospitalization (OR, 8.3; 95%, CI, 2.1–33.4) were also related to higher risk, after adjusting for demographic characteristics. Reliance on emergency department services for urgent asthma care was also associated with a greater likelihood of hospitalization (OR, 3.2; 95% CI, 1.0–9.8). In multivariate analysis not controlling for asthma severity, low income was even more strongly related to hospitalization (OR, 1.2 per $10,000 decrement; 95% CI, 1.02–1.4). Conclusion In adult asthmatics with access to health care, non-white race, low income, and greater asthma severity were associated with a higher risk of hospitalization. Targeted interventions applied to high-risk asthma patients may reduce asthma morbidity and mortality.',
  'Medicine & Public Health, Pneumology/Respiratory System'],
 ['Article',
  'doi:10.1186/gb-spotlight-20001229-01',
  'en',
  'http://dx.doi.org/10.1186/gb-spotlight-20001229-01',
  'Calling all binding sites',
  'Wells, William',
  'Genome Biology',
  'false',
  '10.1186/gb-spotlight-20001229-01',
  'BioMed Central',
  '2000-12-29',
  'Journal',
  '1474-760X',
  '1',
  '1',
  'OriginalPaper, Research news',
  '1',
  '2',
  '13059',
  '©2000 BioMed Central Ltd',
  '',
  'Life Sciences, Animal Genetics and Genomics, Human Genetics, Plant Genetics and Genomics, Microbial Genetics and Genomics, Bioinformatics, Evolutionary Biology']]
columns=['contentType', 'identifier', 'language', 'url', 'title', 'creators',
       'publicationName', 'openaccess', 'doi', 'publisher', 'publicationDate',
       'publicationType', 'issn', 'volume', 'number', 'genre', 'startingPage',
       'endingPage', 'journalId', 'copyright', 'abstract', 'subjects']


class TestCheckParameters(object):
    """
    A class of tests for the function check_parameters

    ...

    Methods
    -------
    test_api_key_error()
        Checks if entering a non-string value for api_key in the check_parameters function will raise a TypeError
    test_number_of_results_error_1()
        Checks if entering a non-integer for number_of_results in the check_parameters function will 
        raise a TypeError
    test_number_of_results_error_2()
        Checks if entering an integer over 100 for number_of_results in the check_parameters function will 
        raise a ValueError
    test_api_key_error()
        Checks if entering a wrong value as a dictionary key for kwargs_dict in the check_parameters 
        function will raise a TypeError
    """
    def test_api_key_error(self):
        """
        Checks if entering a non-string value for api_key in the check_parameters function will raise a TypeError
        """
        with pytest.raises(TypeError):
            check_parameters(1000, 10, {'year':2000})

    def test_number_of_results_error_1(self):
        """
        Checks if entering a non-integer for number_of_results in the check_parameters function will 
        raise a TypeError
        """
        with pytest.raises(TypeError):
            check_parameters('apikey', '10', {'year':2000})
            
    def test_number_of_results_error_2(self):
        """
        Checks if entering an integer over 100 for number_of_results in the check_parameters function will 
        raise a ValueError
        """
        with pytest.raises(ValueError):
            check_parameters('apikey', 105, {'year':2000})
            
    def test_kwargs_error(self):
        """
        Checks if entering a wrong value as a dictionary key for kwargs_dict in the check_parameters 
        function will raise a TypeError
        """
        with pytest.raises(ValueError):
            check_parameters('apikey', 10, {'month':12})

@pytest.fixture
def test_df():
    """
    Sets up a DataFrame for use in later tests.
    """
    df = ResultsAnalysis(pd.DataFrame(df_list, columns=columns))
    return df

def test_RA_search_column(test_df):
    """
    Checks if entering an inappropriate value for the column parameter
    for search_column (a ResultsAnalysis member function) will raise a ValueError
    """
    with pytest.raises(ValueError) as errorinfo:
        test_df.search_column('hi', 'or', 'etc.')
 

def test_RA_add_row(test_df):
    """
    Checks if entering an inappropriate value as a key in the dictionary argument
    for add_row (a ResultsAnalysis member function) will raise a ValueError
    """
    with pytest.raises(ValueError) as errorinfo:
        test_df.add_row({'hello':10})
 


