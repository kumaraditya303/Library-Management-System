#!/bin/env python
"""
This script runs the Library_Management_System application using a development server.
"""

import os

from werkzeug.security import generate_password_hash

from Library_Management_System import app as application
from Library_Management_System import db
from Library_Management_System.models import User
from Library_Management_System.views import main

application.register_blueprint(main)
if __name__ == "__main__":
    db.create_all()
    admin_user = User(
        email="test@domain.com",
        password=generate_password_hash("Test&Test", method="sha256"),
        admin=True,
    )
    db.session.add(admin_user)
    db.session.commit()
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    application.run(HOST, PORT, threaded=True)
