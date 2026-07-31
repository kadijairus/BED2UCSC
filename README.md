<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [BED2UCSC](#bed2ucsc)
  - [About](#about)
  - [Features](#features)
  - [How To Use](#how-to-use)
  - [Development](#development)
    - [Getting Started](#getting-started)
    - [Tests](#tests)
  - [Credits](#credits)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# BED2UCSC

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## About

A tool to upload custom BED-files as UCSC Genome Browser Custom Tracks

## Features

- Adds single BED file to UCSC Genome Browser

## How to Use

Add a bookmark to your Chrome browser:
Name: Upload BED
URL:
```sh
javascript:(async()=>{try{let r=await fetch('http://127.0.0.1:8585/data');if(!r.ok)throw new Error('Local server not running');let txt=await r.text();let a=document.querySelector('textarea[name="hgct_customText"]');if(a){a.value=txt;let b=document.querySelector('input[name="hgct_doSubmit"]');if(b)b.click();else document.forms[0].submit();}else{alert("Please navigate to the UCSC Custom Track page first.");}}catch(e){alert("Error fetching local BED data: "+e.message);}})();
```

## Development

### Getting Started
First, [fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html) this repository to your namespace, then fire up your command prompt and ...

1. Clone the forked repository
2. Navigate to the cloned project directory: `cd project_name`
3. activate your python virtual environment and `pip install -r requirements.txt`.
4. `pre-commit install`
5. `pre-commit install --hook-type commit-msg`
6. `pre-commit run --all-files`

Now you can start working on the code.

### Tests

Simply run `pytest`. For more detailed output, including test coverage:

```sh
pytest -vv --cov=. --cov-report term-missing
```

## Credits

This project was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`engineervix/cookiecutter-pyproject`](https://github.com/engineervix/cookiecutter-pyproject) project template.

----
