#!/bin/env python
"""
This script runs the Library_Management_System application using a development server.
"""

import os

from Library import app as application
from Library import db
from Library.views import main

application.register_blueprint(main)
db.create_all()
if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "9000"))
    except ValueError:
        PORT = 9000
    application.run(HOST, PORT, threaded=True)
