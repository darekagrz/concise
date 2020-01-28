It assumes you pulled source into c:\Projects\concise folder
1. Download chromedriver version matching chrome version from http://chromedriver.storage.googleapis.com/index.html and copy it to C:\Projects\concise\externals folder
2. Download python installer from https://www.python.org/downloads/release/python-381/
3. Install python from downloaded installer - select checkbox 'Add Python to environment variables' (that makes next steps easier)
4. After succesful python installation open command line
5. Create virtual environment by running command: python -m venv c:\autotest
6. Navigate to c:\autotest\Scripts and execute activate.bat 
7. Install pip by running command: pip install -U pip
8. Install automation script required packages by running command: pip install -U -r C:\Projects\concise\requirements.txt
9. In the same command line navigate to C:\Projects\concise\spotify\tests and execute pytest --html=demo.html test_demo.py 
