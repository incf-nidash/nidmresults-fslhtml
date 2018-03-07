Create HTML output of NIDM-Results files (In an FSL-like format).

##### Requirements

As the viewer requires the CSS styling for FSL output pages and recreates FSL displays, it assumes FSL (version 5.0 or above) is installed. Full installation details for fsl are found here:

https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation

##### Usage

```
$ nidmviewerfsl -h
usage: nidmviewerfsl [-h] [--d] nidmFile outFolder

NIDM-Results Viewer

positional arguments:
  nidmFile    NIDM-Results Turtle file
  outFolder   Destination folder for HTML pages

optional arguments:
  -h, --help  show this help message and exit
```

##### Install via pip

The viewer can be installed via pip through:
```
pip install https://github.com/incf-nidash/nidmresults-fslhtml.git@master
```

##### Install via git

Alternatively, instalation is possible via cloning from github like so:
```
git clone https://github.com/incf-nidash/nidmresults-fslhtml.git
```
And then running the `setup.py` file as follows:
```
python setup.py
```
##### Tests
To run the tests from the commandline use the following commands:
```
	python nidmviewerfsl/tests/test_fslViewer.py
	python nidmviewerfsl/tests/testError.py
```

The output of the tests will appear in the folders given in `nidmviewerfsl/tests/data`.
