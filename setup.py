from setuptools import setup, find_packages

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
    license="BSD",
    keywords="Prov, NIDM, Provenance",
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
    package_data={'nidmviewerfsl':
                  ['queries/*.txt',
                   'templates/*.nii']},
    include_package_data=True,
    install_requires=requirements
)
