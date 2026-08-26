
# CONP Portal
[![Coverage Status](https://coveralls.io/repos/github/CONP-PCNO/conp-portal/badge.svg?branch=master)](https://coveralls.io/github/CONP-PCNO/conp-portal?branch=master)

- [Installation](#installation)
	- [Requirements](#requirements)
	- [Clone the repository](#clone-the-repository)
	- [Setup Python Virtual Environment](#setup-python-virtual-environment)
	- [Setup Flask Environment](#setup-flask-environment)
	- [Initilize the test database](#initilize-the-test-database)
- [Run Application](#run-application)
	- [Using Flask Locally](#using-flask-locally)
	- [AWS Cloud9 (Experimental)](#aws-cloud9-experimental)
- [Docker](#docker)
- [Developer and Contributor Information](#developer-and-contributor-information)
	- [Experiments Portal](#experiments-portal)
	- [Testing Code](#testing-code)
	- [Coding Standards](#coding-standards)
- [Deployment](#deployment)
- [License](#license)
- [Credits](#credits)

## Installation

### Requirements

- Python v3.10 through v3.14 (inclusive). To check the version(s) you may have
installed open a terminal and type `python3 -V`.
- NodeJS v16 - The CONP Portal front-end uses React.
- datalad
- git-annex (on debian `apt-get -y install git-annex-standalone`)
- sqlite3, mysql or mariadb
- (optional) [`pyenv`](https://github.com/pyenv/pyenv) v2.8.4

#### Optionally install pyenv and python

    pip install pyenv
    # Usage Example, using python 3.12
    pyenv install 3.12
    pyenv local 3.12
    pyenv shell 3.12

### Clone the repository

    git clone https://github.com/CONP-PCNO/conp-portal.git conp-portal
    cd conp-portal

### Setup Python Virtual Environment

The environment name is flexible; common conventions include `.venv`, `venv`, or version-specific names like `.venv-py314`

Create a Python virtual environment called `.venv`
and install the python dependencies.

In the top level directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --require-virtualenv --requirement requirements.txt
```

### Setup Flask Environment

You can set environment variables in the `.env` or `.flaskenv` file.  A template is provided for you to start from in the top level directory:

```bash
cp flaskenv.template .flaskenv
```

You will need to specify a database environment to use.  The easiest for testing purposes is sqlite3
which is a filebased database system that will run locally on your system.

First you will need to make sure you install sqlite3 for you system. Information can be found at https://www.sqlite.org/index.html.

For linux we recommend using the packaged version that comes from your distribution. To make sure it installed, you can run from the terminal `sqlite3`
and the application should run. Type `.q` and return to exit.

#### Edit the DATABASE_URL

In .flaskenv, replace the words `<ENTER FLASK TOP DIR>` with path to your top level flask directory.  You should already be in it, so you can find the path with `pwd`.

### Initilize the test database

We provide some initial data for you to create a functioning database
for testing purposes.  The following commands perform data bootstrap
and index population. These are **one-time setup steps** that may take
several minutes to complete.

In the top level directory:

```bash
python -m flask db upgrade
python -m flask seed_test_db
python -m flask update_pipeline_data
python -m flask seed_test_experiments
```

If using a python environment, try `./venv/bin/python3 -m flask <command>` instead.

**Note:** `flask update_pipeline_data` and `flask seed_test_db` download
and process large datasets from remote repositories. These are setup-only
commands and should not be run repeatedly during development.

## Run Application

### Using Flask Locally

In the top level directory:

```bash
flask run
```

The application should now be live on `http://localhost:5000/`

### AWS Cloud9 (Experimental)

See [docs/AWS_Cloud9.md](./docs/AWS_Cloud9.md).

## Docker

This application supports Python 3.12 through 3.14 (inclusive) and defaults to Python 3.14 in Docker.

```bash
# Builds a Docker image from a Dockerfile
# for a specific Python version (3.12 to 3.14) and
# Tags (names) the resulting image conp-portal:py3.12
# Default is 3.12
docker build --build-arg PYTHON_VERSION=3.12 -t conp-portal:py3.12 .
# Example: build for Python 3.14
# docker build --build-arg PYTHON_VERSION=3.14 -t conp-portal:py3.14 .

# Run the Container
# in detached mode (in the background)
docker run -d --name my-conp-portal -p 4000:4000 -p 8080:8080 -v ${PWD}/app:/app/app --rm conp-portal:py3.12

# Start dev frontend inside the running container (adjust container id)
docker exec -it my-conp-portal bash -c "cd /app/app/static/v2 && yarn dev"
```

**Note:** The Dockerfile uses `requirements.txt` for dependencies (same as the development environment).

## Developer and Contributor Information

### Experiments Portal

If you would like to run the run the experiments portal with hot module replacement, in a separate terminal run:

    npm start --prefix app/static/lib/experiments-portal

To build the experiments portal, run:

    npm run build --prefix app/static/lib/experiments-portal

### Testing Code

We use the `pytest` framework for testing all aspects of the application. This will be automatically run by CI workflows when a pull request is made.

The tests exists in the `tests/` directory and should not effect any of the development or production builds to run. Please feel free to add unit and functional tests with any new feature.  Pytest will automatically pick up any tests that start with `test_` that are placed in the folder under a directory.  Please adhere to the structure there.

- For unit tests of classes and utilities, use the folder `tests/unit_tests`.
- For database specific testing, please use the folder `tests/database_tests`.
- For blueprint and route testing, please use the `tests/blueprint_specific_tests` folder and place it in the appropriate blueprint specific directory.

### Coding Standards

In order to keep the Python code maintainable and readable, please run `./lint.sh` to make sure the coding is up to standards.

## Deployment

See [deploy documentation](deploy/README_deploy.md).

## License

[MIT License](./LICENSE)

## Credits

[Humans](./humans.md) at the [Canadian Open Neuroscience Platform](https://conp.ca/).
