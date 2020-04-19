"""
This script runs the Library_Management_System application using a development server.
"""

from os import environ
from Library_Management_System import app as application
from Library_Management_System import db

if __name__ == '__main__':
    db.create_all()
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    application.run(HOST, PORT, threaded=True)
