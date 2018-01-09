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

##### Install from source
```
pip install https://github.com/incf-nidash/nidmresults-fslhtml.git@master
```

##### Tests
To run the tests:
```
	Tests\test_fslViewer.py
	Tests\testError.py
```
