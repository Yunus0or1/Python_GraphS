from cx_Freeze import setup, Executable
import cx_Freeze
from multiprocessing import queues
import idna.idnadata
import sys,os

base = None

if sys.platform == "win32":
    base = "Win32GUI"



executables = [cx_Freeze.Executable("GraphS.py", base=base,icon = "GraphS.ico")]
os.environ ['TCL_LIBRARY'] ='C:\\Users\\Yunus\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6'
os.environ ['TK_LIBRARY'] ='C:\\Users\\Yunus\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6'

packages = ["tkinter","matplotlib.pyplot","numpy","math","mysql.connector","django.db","MySQLdb","matplotlib","mysql","pandas"]
options = {
    'build_exe': {
        'packages':packages,
        "include_files": ["tcl86t.dll", "tk86t.dll"],

    },
}

setup(
    name = "GraphS",
    version = "1.0",
    options = options,
    description = 'Nothing',
    executables = executables
)