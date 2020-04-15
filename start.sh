#!/bin/bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=runserver.py
flask run
