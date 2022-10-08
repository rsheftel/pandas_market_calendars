@ECHO OFF
REM Makes the Sphinx documentation files from the Jupyter Notebook examples

FOR %%a IN (%~dp0\.) do set SOURCE=%%~dpa
set OLD_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;%SOURCE%

jupyter nbconvert --to rst --execute --output-dir . --output usage.rst ..\examples\usage.ipynb
set PYTHONPATH=%OLD_PYTHONPATH%
