# -*- coding: utf-8 -*-
"""WSGI entry point for PythonAnywhere.

On PythonAnywhere, edit the web app's WSGI configuration file to import
``application`` from this module, e.g.:

    import sys
    path = '/home/<youruser>/Silex-elevators'
    if path not in sys.path:
        sys.path.insert(0, path)
    from wsgi import application
"""
from app import app as application

if __name__ == "__main__":
    application.run()
