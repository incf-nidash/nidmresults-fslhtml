from setuptools import setup, find_packages
import pip

#nipy and matplotlib need pip installation as setup.py does not install their dependencies correctly.
pip.main(["install",'nipy'])
pip.main(["install",'nilearn'])
pip.main(["install",'matplotlib'])
pip.main(["install",'sklearn'])
pip.main(["install",'zlib'])
pip.main(["install",'Pillow'])

readme = "Empty for now"

reqs = [line.strip() for line in open('requirements.txt').readlines()]
requirements = list(filter(None, reqs))

setup(
    name="nidmfslhtml",
    version="0.0.1",
    author="Peter Williams",
    scripts=['bin/nidmviewerfsl'],
    author_email="p.williams.2@warwick.ac.uk",
    description=(
        "Viewing of NIDM-Results packs through FSL HTML results pages."),
    license = "BSD",
    keywords = "Prov, NIDM, Provenance",
    packages=find_packages(),
    package_dir={
        'nidmviewerfsl': 'nidmviewerfsl'
    },
    long_description=readme,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    package_data={'':
                  ['Queries/checkExtentThreshold.txt']},
    include_package_data=True,
    install_requires=requirements
)
