#!/bin/env python
"""
This script runs the Library_Management_System application using a development server.
"""

import os

from Library_Management_System import app as application
from Library_Management_System import db
from Library_Management_System.views import main

application.register_blueprint(main)
db.create_all()
if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    application.run(HOST, PORT, threaded=True)
