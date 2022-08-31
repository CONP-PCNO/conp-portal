
# CONP Portal 
[![Build Status](https://travis-ci.org/CONP-PCNO/conp-portal.svg?branch=master)](https://travis-ci.org/CONP-PCNO/conp-portal)
[![Coverage Status](https://coveralls.io/repos/github/CONP-PCNO/conp-portal/badge.svg?branch=master)](https://coveralls.io/github/CONP-PCNO/conp-portal?branch=master)
### Requirements

This code requires Python 3.7 

### Python Virtual Environment

Create a Python virtual environment called `venv` and install Flask dependencies

In the top level directory:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Initialize the flask environment

You can set environment variables in the .flaskenv file.  A template is provided for you to start from.

In the top level directory:

```shell
cp flaskenv.template .flaskenv
```

You will need to specify a database environment to use.  The easiest for testing purposes is sqlite3
which is a filebased database system that will run locally on your system.

First you will need to make sure you install sqlite3 for you system. Information can be found at https://www.sqlite.org/index.html.
For linux we recommend using the packaged version that comes from your distribution. To make sure it installed, you can run from the terminal `sqlite3`
and the application should run. Type `.q` and return to exit.

Edit the DATABASE_URL 

In .flaskenv, replace the words `<ENTER FLASK TOP DIR>` with path to your top level flask directory.  You should already be in it, so you can find the path with `pwd`.

### Initilize the test database

We provide some initial data for you to create a functioning database for testing purposes.  To initialize this:

In the top level directory:

```shell
flask db upgrade
flask seed_test_db
flask update_pipeline_data
flask seed_test_experiments
```

### Run Application

In the top level directory:

```shell
flask run
```

The application should now be live on `http://localhost:5000/` 
    
### Testing

We use the pytest framework for testing all aspects of the application. This will be automatically run by TravisCI when a pull request is made.  

The tests exists in the `tests` directory and should not effect any of the development or production builds to run. Please feel free to add unit and functional tests with any new feature.  Pytest will automatically pick up any tests that start with `test_` that are placed in the folder under a directory.  Please adhere to the structure there.

For unit tests of classes and utilities, use the folder `tests/unit_tests`
For database specific testing, please use the folder `tests/database_tests`
for blueprint and route testing, please use the `tests/blueprint_specific_tests` folder and place it in the appropriate blueprint specific directory.

### Coding standards

In order to keep the Python code maintainable and readable, please run `./lint.sh` to make sure the coding is up to standards. TravisCI will be checking this.

### AWS Cloud9 (Experimental)

Some experimental testing cases are being explored with AWS Cloud 9.

To run the application on a Cloud9 instance:

```bash
    flask run --host=0.0.0.0 --port=8080
```

### Deployment
    
This flask application is deployed on Heroku. More information will be available soon
