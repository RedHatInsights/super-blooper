# Super Blooper

Super Blooper is a tool for comparing two graphql outputs to gather data about namespaces in openshift

## Setup

Install the project with pip:

```pip install .```

## Running the Script

To run the script you must provide a JSON file containing the query for the graphql
endpoint.

You must also configure the `config.yml` file with the endpoints for your graphql resources as well as a
list of namespaces you want the info on. A [config-example.yml](config-example.yml) has been provided to get
you started with the format. Rename this file to `config.yml` when ready to execute.

### Usage

```sh
usage: bloop.py [-h] --file FILE [--config CONFIG]

options:
  -h, --help       show this help message and exit
  --file FILE      Input query file path.
  --config CONFIG  Path to config.yml
```