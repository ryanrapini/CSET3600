import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files = ['resources'])

executables = [
    Executable('E:\\Documents\\GitHub\\CSET3600\\main.py', 'Console', targetName = 'battleship.exe')
]

setup(name='Battleship',
      version = '1.0',
      description = 'Battleship, the game!',
      options = dict(build_exe = buildOptions),
      executables = executables)