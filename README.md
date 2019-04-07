
# CONP Portal 

### Requirements

This code requires Python 3.7 

### Python Virtual Environment

Create a Python virtual environment called `venv` and install Flask dependencies

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Run Application

You can run the application locally with 

    flask run
    
The application will be live on `http://127.0.0.1:5000/`
    

### Get the dataset repository

       git clone git@github.com:CONP-PCNO/conp-dataset data

The search will be executed on this `data` repository 

### AWS Cloud9 (Experimental)

Some experimental testing cases are being explored with AWS Cloud 9.

To run the application on a Cloud9 instance:

```python
    flask run --host=0.0.0.0 --port=8080
```


### Deployment
    
This flask application is deployed on Heroku. More information will be available soon