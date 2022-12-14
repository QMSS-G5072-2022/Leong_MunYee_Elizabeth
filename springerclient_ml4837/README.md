# springerclient_ml4837

An API wrapper for the Springer Nature API, allowing users to query Springer’s database of scientific and academic documents.

## Installation

```bash
$ pip install springerclient_ml4837
```

## Usage

This project is meant for use with the Springer Nature API, which requires an API key.

Head over to the Springer Nature API portal to sign up for a key: https://dev.springernature.com/

This package contains a function, display_springer_constraints, which displays the constraints that users can use to limit the results returned by an API call.

This allows users to make use of the most important function in this package, search_nature, which allows users to make API calls with constraint parameters. This returns a DataFrame.

Users can then use search_nature to instantiate an instance of the class, ResultsAnalysis. The ResultsAnalysis class represents a dataframe containing the results of an API call. Further searches and other forms of analysis can be done on the instantiated object, by using member functions of this class. This includes potting histograms based on the columns of the dataframe, adding entries, and searching columns for keywords.


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`springerclient_ml4837` was created by Mun Yee Elizabeth LEONG. It is licensed under the terms of the MIT license.

## Credits

`springerclient_ml4837` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
