import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [cx_Freeze.Executable("port_scanner.py",base=base)]

cx_Freeze.setup(
    name = 'port_scanner',
    options = {'build_exe': {'packages':['tkinter','socket','threading']}},
    version = '1.0',
    description = 'Scan open ports',
    executables = executables
)