from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("qtiConverterApp.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "qtiConverterApp",
    options = options,	
    version = "0.1",
    description = 'Converts txt file to QTI for Canvas quiz',
    executables = executables
)