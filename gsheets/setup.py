import setuptools


with open("README.md","r") as fh:
    long_description = fh.read()
    

    
setuptools.setup(
    name="gsheets",
    version="0.0.1",
    author="DevarakondaV",
    author_email="",
    description="Pushes values to spreadsheet on google sheets",
    long_description=long_description,
    long_dscription_content_type="text/markdown",
    url="github-repo",
    package=setuptools.find_packages(),
    install_requires=[
        'google-api-python-client',
        'oauth2client',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operationg System :: OS Independent",
    ],
)
    