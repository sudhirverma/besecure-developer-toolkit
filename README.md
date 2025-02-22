# Be-Secure Developer Toolkit (bes-dev-kit)

bes-dev-kit is a cli tool for generating metadata and assessment report for [BeSLighthouse](https://github.com/Be-Secure/BeSLighthouse).

# Pre-requisites

1. Python 3.10
2. pip
3. Github personal access token

# Installation

`$ python3 -m pip install besecure-developer-toolkit`

# Usage

If you are running the command for the first time, you will be prompted to provide the complete path to your `besecure-osspoi-datastore` and `besecure-assessment-datastore` and your `personal access token`

### Generate Metadata

Command helps to generate metadata such as OSSP-master file data and version details file.

`$ bes-dev-kit generate metadata`

![generate metadata](docs/generate_metadata.gif)

For more options use `--help` at end.

![metadata help](docs/metadata_help.gif)

### Generate Reports

`$ bes-dev-kit generate report <report name>`

![generate report](docs/generate_report.gif)

`<report name> - scorecard, codeql, criticality_score`

For more options use `--help` at end.

![report help](docs/generate_report_help.gif)

`Note: All three reports can be generated at once by passing all report names - $ bes-dev-kit generate report scorecard criticality_score codeql`

# Setting up locally

1. Install [poetry](https://python-poetry.org/). Use the [link](https://python-poetry.org/docs/) to install Poetry.
2. Clone the repo.
3. Move into the cloned directory.
4. Run the command - `$ poetry add "typer[all]"`
5. Create a new virtual env using Poetry - `$ poetry shell`
6. Run the command to install the tool- `$ poetry install`
7. Check installation - `$ bes-dev-kit --help`


