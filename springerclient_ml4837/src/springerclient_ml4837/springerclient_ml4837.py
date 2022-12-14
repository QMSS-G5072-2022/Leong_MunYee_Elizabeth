import requests
import pandas as pd
import requests.exceptions
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def display_springer_constraints(constraints_url='https://dev.springernature.com/adding-constraints', table_number=1):
    """
    Produce a table of the constraints that can be used to query the Springer API. This is done by scraping the HTML of the Springer Nature API query constraints page.

    Parameters
    ----------
    constraints_url: str. The URL from which the constraints table is scraped. This is set to the current URL by default, but this URL may change in the future.
    
    table_number: int. The number of the table on the webpage that contains the query constraints. This is set to 1 by default as currently, the table of interest is the 1st table on the website.
    
    Returns
    -------
    constraints_table. The table of the constraints that can be used to query the Springer API. 

    Examples
    --------
    >>> display_springer_constraints()
    pandas.DataFrame
        Columns:
            Name: Constraint, dtype=object
            Name: Description, dtype=object
            Name: Applies to collection	, dtype=object
            Name: Example Query, dtype=object
    """
    constraints_table = pd.read_html(constraints_url)[table_number - 1]
    constraints_table.columns = constraints_table.iloc[0]
    constraints_table = constraints_table.drop(constraints_table.index[0])
    return constraints_table

def generate_search_url(url, api_key, number_of_results, constraints_dict):
    """
    Generates a URL string that will be used in the API GET request.

    Parameters
    ----------
    url: str. The base URL for the API GET request.
    api_key: str. The API key needed for authentication.
    number_of_results: int. The number of results to return in the API GET request.
    constraints_dict: dict. Its keys must be constraint names specified by Springer, which must be strings. The values are the search terms specific to that constraint.

    Returns
    -------
    search_url. The URL string that will be used to send the API GET request.

    Examples
    --------
    >>> generate_search_url('https://api.springernature.com/metadata/json', 'key101010', 10, {'year': 2000, 'subject': 'Chemistry'})
    'https://api.springernature.com/metadata/json?q=year:2000 subject:Chemistry&api_key=key101010&p=10'
    """
    
    url = url 
    api_key = api_key
    constraints_dict = constraints_dict
    constraints_joined = {str(key)+  ":" : str(val) + " " for key, val in constraints_dict.items()}
    concat_params = ''.join([i for k,v in constraints_joined.items() for i in [k, str(v)]])
    search_url = url + '?q=' + concat_params.strip() + "&api_key=" + api_key + "&p=" + str(number_of_results)
    return search_url

def get_url_series(urls_column):
    """
    Returns a pandas Series of URLs, from a list of dictionaries of the format \"{[{'format': '', 'platform': '', 'value': 'http:...'}\".
    This function is not meant for the user, but to process a column in the dataframe containing the JSON response to the GET request from Springer Nature
    
    Parameters
    ----------
    urls_column: list. A list of lists containing dictionaries. This code is written specifically to process a column in the dataframe containing the JSON response to the GET request from Springer Nature.
    
    Returns
    -------
    url_Series. A pandas Series of URLs.

    Examples
    --------
    >>> get_url_list([[{'format': '', 'platform': '', 'value': 'http://dx.doi.org/10.1186/gb-spotlight-20001229-02'}], [{'format': '', 'platform': '', 'value': 'http://dx.doi.org/10.1186/gb-2000-2-1-interactions0001'}]])
    0    http://dx.doi.org/10.1186/gb-spotlight-20001229-02
    1    http://dx.doi.org/10.1186/gb-2000-2-1-interactions0001
    dtype: object
    """  
    
    newurllist = []
    for list_of_dicts in urls_column:
        i = 0
        if not isinstance(list_of_dicts, float):
            while i < len(list_of_dicts):
                kv_pair = dict(list_of_dicts[i])
                url = kv_pair['value']
                i+=1
        newurllist.append(url)
    url_Series = pd.Series(newurllist)
    return url_Series

def get_creators_series(creator_column):
    """
    Returns a pandas Series of creators' names concatenated with commas. This function is not meant for the user, but to process a column in the dataframe containing the JSON response to the GET request from Springer Nature.
    
    Parameters
    ----------
    creator_column: list. A list of lists containing dictionaries.
    
    Returns
    -------
    creators_Series. A pandas Series of URLs.

    Examples
    --------
    >>> get_creators_series([[{'creator': 'Wells, William'}], [{'creator': 'Iliopoulos, Ioannis'}, {'creator': 'Tsoka, Sophia'}, {'creator': 'Andrade, Miguel A'}, {'creator': 'Janssen, Paul'}, {'creator': 'Audit, Benjamin'}, {'creator': 'Tramontano, Anna'}, {'creator': 'Valencia, Alfonso'}, {'creator': 'Leroy, Christophe'}, {'creator': 'Sander, Chris'}, {'creator': 'Ouzounis, Christos A'}]])
    0                                       Wells, William
    1    Iliopoulos, Ioannis; Tsoka, Sophia; Andrade, Miguel A; Janssen, Paul...
    dtype: object
    """   
    newcreatorlist = []
    for list_of_dicts in creator_column:
        i = 0
        list_of_author_names = []
        if not isinstance(list_of_dicts, float):
            while i < len(list_of_dicts):
                kv_pair = dict(list_of_dicts[i])
                author_name = kv_pair['creator']
                list_of_author_names.append(author_name)
                i+=1
        author_names = '; '.join(list_of_author_names)
        newcreatorlist.append(author_names)
    creators_Series = pd.Series(newcreatorlist)
    return creators_Series

def check_parameters(api_key, number_of_results, kwargs_dict):
    """
    Checks whether parameters intended for the function search_nature are valid. Raises errors if inappropriate values exist.
    This function is not meant for the user, but for use within the main function of this package, search_nature.
    
    Parameters
    ----------
    api_key: any type. The value for the API key passed to search_nature.
    number_of_results: any type. The value for the number of results passed to search_nature
    kwargs_dict: dict. The dictionary of keyword arguments passed to search_nature.
    
    Returns
    -------
    None. In the case where all parameters are valid.
    TypeError. In the case where a parameter has a type error.
    ValueError. In the case where a parameter has a type error.

    Examples
    --------
    >>> check_parameters(1000, 10, {'year':2000})
    TypeError: api_key parameter must be a string

    >>> check_parameters('apikey', 105, {'year':2000})
    ValueError: 105 is more than the maximum number of results we can make in a single API request
    """
    
    # Check that api_key is a string
    if type(api_key) is not str:
        raise TypeError("api_key parameter must be a string") 
    
    # Check number of results wanted in query; max is 100
    if type(number_of_results) is not int:
        raise TypeError("number_of_results parameter must be an integer")
    if number_of_results > 100:
        raise ValueError(f"{number_of_results} is more than the maximum number of results we can make in a single API request")

    # Check that search parameters in kwargs_dict are valid
    for key in kwargs_dict.keys():
        if str(key) not in ['doi','subject','keyword','language','pub','year','onlinedate','country','isbn','issn','journalid','topicalcollection','journalonlinefirst','date','issuetype','issue','volume','type','openaccess']:
            raise ValueError(f"'{key}' is not a valid search field. The valid search fields are:\ndoi, subject, keyword, language, pub, year, onlinedate, country, isbn, issn, journalid, topicalcollection, journalonlinefirst, date, issuetype, issue, volume, type, openaccess")

def search_nature(api_key, number_of_results, **kwargs):
    """
    Returns a dataframe comprising the search results of the API GET request to Springer Nature's API.

    Parameters
    ----------
    api_key: string. The API key needed for authentication.
    number_of_results: int. The number of results to return in the API GET request.
    **kwargs: int or str. The keywords should be the name of the search constraint, and the value should be the search term. All valid search constraints may be found at https://dev.springernature.com/adding-constraints or by running the function display_springer_constraints()
    
    Returns
    -------
    results. The dataframe comprising the search results of the API GET request to Springer Nature's API.

    Examples
    --------
    >>> search_nature('redacted_api_key', 2, year=2000, language='en')
    pandas.DataFrame
        Columns:
            Name: contentType, dtype=object
            Name: identifier, dtype=object
            Name: language, dtype=object
            Name: url, dtype=object
            Name: title, dtype=object
            Name: creators, dtype=object
            Name: publicationName, dtype=object
            Name: openaccess, dtype=object
            Name: doi, dtype=object
            Name: publisher, dtype=object
            Name: publicationDate, dtype=object
            Name: publicationType, dtype=object
            Name: issn, dtype=object
            Name: volume, dtype=object
            Name: number, dtype=object
            Name: genre, dtype=object
            Name: startingPage, dtype=object
            Name: endingPage, dtype=object
            Name: journalId, dtype=object
            Name: copyright, dtype=object
            Name: abstract, dtype=object
            Name: subjects, dtype=object
    """
    check_parameters(api_key, number_of_results, kwargs)
    url = 'https://api.springernature.com/metadata/json'
    api_key = api_key
    search_url = generate_search_url(url, api_key, number_of_results, kwargs)
    
    print(search_url)
    # GET request
    try:
        r = requests.get(search_url) # Code for the GET request
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') # Check (and show) the status of the request.
    except Exception as err: 
        print(f'Other error occurred: {err}') 
    else:
        print('Request was a success! \nThe response type is: ' + str(r.headers['content-type'])) # Check (and show) the type of the response (e.g. XML, JSON, csv).

    json_r = r.json() 
    results = pd.DataFrame(json_r['records'])
   
    # Formatting the URLs and the creators
    urls_column = [url_list for url_list in results['url']]
    results['url'] = get_url_series(urls_column)
    
    creators_column = [creators for creators in results['creators']]
    results['creators'] = get_creators_series(creators_column)
    
    return results

class ResultsAnalysis:
    """
    A class used to represent a dataframe containing the results of an API call

    ...

    Attributes
    ----------
    results_df : pandas.DataFrame
        a DataFrame. User can use this to hold the results of the API call.
    colnames : pandas.Index
        the column names of the DataFrame results_df
    colnames_string : str
        a string representation of all the column names of the DataFrame results_df

    Methods
    -------
    print_head()
        Prints the head of results_df
    print_columns()
        Prints all the columns of results_df
    print_specific_column(column)
        Prints the column, specified by the parameter 'column', of results_df
    explode_csv(exploding_column)
        Returns an exploded DataFrame based on the column specified by the parameter, 'exploding_column'
    plot_histogram(column)
        Shows a histogram of results_df based on a column, specified by the parameter 'column'.
        Only some columns are able to produce meaningful histograms. These are: 'contentType',
        'language', 'publicationName', 'openaccess', 'publisher', 'publicationType', 'genre', 'subjects'. 
        Specifiying other values will raise a ValueError.
    search_column(column, *args, or_and='or')
        Returns a DataFrame subset of results_df, for which the column (specified by the parameter 'column') 
        contains any or all (depending on the value of or_and specified) of the search terms specified in *args. 
        or_and defaults to 'or'.
    add_row(entry)
        Appends an additional row, 'entry', to the DataFrame results_df
    remove_rows(n):
        Deletes the last n rows as specified by the user from results_df.
    save_as_csv(file_name)
        Saves results_df as a CSV file
    """
    def __init__(self, results_df):
        self.results_df = results_df
        self.colnames = self.results_df.columns 
        self.colnames_string = ', '.join(self.results_df.columns) 
    
    def print_head(self):
        """
        Prints the head of results_df
        
        Returns
        -------
        None
        """
        print(self.results_df.head())
    
    def print_columns(self):
        """
        Prints the columns of results_df
        Returns
        -------
        None
        """
        print(self.colnames)    
    
    def print_specific_column(self, column):
        """Prints a column of results_df

        Parameters
        ----------
        column : str
            The column of results_df to be printed.
        
        Returns
        -------
        None
        """
        print(self.results_df[column])
    
    def explode_csv(self, exploding_column):
        """Splits a pandas cell containing comma-separated values into multiple rows. 
        This function is not intended for the user but as a function to be used in the plot_histogram function. 

        Parameters
        ----------
        exploding_column : str
            The column of results_df to be exploded.

        Returns
        -------
        exploded_df : DataFrame
            The exploded DataFrame.
        """        
        exploded_df = self.results_df.explode(exploding_column)
        return exploded_df
    
    def plot_histogram(self, column):
        """Shows a histogram of results_df based on a column.

        Parameters
        ----------
        column : str
            The column of results_df, based on which the histogram will be plotted.
        
        Returns
        -------
        None
        """
        if column not in ['contentType','language', 'publicationName', 'openaccess', 'publisher', 'publicationType', 'genre', 'subjects']:
            raise ValueError(f"It is not possible to plot a meaningful histogram using the column '{column}'. Please try the following columns instead:\n'contentType','language', 'publicationName', 'openaccess', 'publisher', 'publicationType', 'genre', or 'subjects'")
        if column in ['genre', 'subjects']:
            exploded_df = self.explode_csv(column)
            exploded_df[column].hist(bins=10)
            plt.title(f"Histogram of the column '{column}'")
            plt.xticks(rotation='vertical')
            plt.show()             
            # https://stackoverflow.com/questions/5615648/how-can-i-call-a-function-within-a-class
        else:        
            self.results_df[column].hist(bins=10)
            plt.title(f"Histogram of the column '{column}'")
            plt.xticks(rotation='vertical')
            plt.show()      

    # smaller searches without having to make request again
    def search_column(self, column, *args, or_and='or'):
        """Returns a DataFrame subset of results_df, based on the user-specified search.

        Parameters
        ----------
        column : str
            The column of results_df that will be searched.
        *args : str
            Search terms for the search. 
        or_and : str
            Whether user wants to conduct an 'or' search (contains ANY of the search terms),
            or an 'and' (contains ALL of the search terms) search. (Default is 'or').

            
        Returns
        ----------
        search_results. A DataFrame subset of results_df, based on the user-specified search.
        """
        if column not in self.colnames:
            raise ValueError(f"There is no column titled '{column}'. Please try the following columns instead:\n" + self.colnames_string)
        if or_and not in ['or', 'and']:
            raise ValueError(f"'{or_and}' is not a valid argument. Please specify:\n'or': if you want to search for entries containing ANY of your search terms.\n'and': if you want to search for entries containing ALL of your search terms.")
        # check that args are all    strings??
        
        # case insensi
        column = column
        search_terms = [arg for arg in args]
        if or_and != 'and':      
            print(f'Entries containing ANY of the following search terms (separated by a comma): ' + ', '.join(search_terms) + f'\nin the column "{column}".')
            self.search_results = self.results_df[np.logical_or.reduce([self.results_df[str(column)].str.contains(search_term, case=False) for search_term in search_terms])]
        if or_and == 'and':   
            print(f'Entries containing ALL of the following search terms (separated by a comma): ' + ', '.join(search_terms) + f'\nin the column "{column}".')
            self.search_results = self.results_df[np.logical_and.reduce([self.results_df[str(column)].str.contains(search_term, case=False) for search_term in search_terms])]
        
        return self.search_results        
    
    def add_row(self, entry):
        """Appends an additional row, 'entry', to the DataFrame results_df. 
        This changes the contents of results_df but DOES NOT push the result to the Springer database.

        Parameters
        ----------
        entry : dict
            A dictionary representing the new entry. Keys must match the columns of results_df, 
            but not all keys have to be used.
        
        Returns
        -------
        results_df: DataFrame
            The results_df with the row appended.
        """
        for key in entry.keys():
            if key not in self.colnames:
                raise ValueError(f"There is no column titled '{key}'. Please specify values for any of the following columns instead:\n" + self.colnames_string + '.\nThe right format is: {\'Column name\':\'value\'}')
        entry = pd.DataFrame([entry]) # https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
        self.results_df = pd.concat([self.results_df, entry], ignore_index=True)
        return self.results_df
    
    def remove_rows(self, n):
        """Deletes the last n rows as specified by the user from results_df. 
        This changes the contents of results_df.

        Parameters
        ----------
        n : int
            The number of rows the user wishes to remove from the tail of results_df
        
        Returns
        -------
        results_df: DataFrame
            The results_df with the n rows removed.
        """
        n = n
        self.results_df = self.results_df[:-n]
        return self.results_df
    
    def save_as_csv(self, file_name):
        """Saves results_df as a CSV file
        
        Parameters
        ----------
        file_name : str
            File name that the CSV file will be saved as. Should end with ".csv".
            
        Returns
        -------
        None
        """
        file_name = file_name
        if file_name[-4:] != '.csv':
            raise ValueError(f"'{file_name}' does not end in '.csv'. Please specify a file_name ending in '.csv'")
  
        self.results_df.to_csv(file_name)
