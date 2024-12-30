"""
This is a setup.py script generated by py2applet

Usage:
    /usr/local/bin/python3 setup.py py2app
"""

from setuptools import setup

APP = ['qtiConverterApp.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True,
            'includes': ['pathlib','opencv-python','matplotlib'],
            'iconfile': 'LargeIconQTI.icns'
            }#,
            #'excludes': "PyQt5, scipy, jupyter, jupyterlab,numpy,pandas,jupyter_console,matplotlib,statsmodels,ipython"}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
