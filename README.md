# Get Currencies from Yahoo Finance

Create a virtual environment with Python 3.9.5 and activate it:

```bash
# For Windows 10 PowerShell (with already installed Python 3.9.5 interpreter)
py -3.9 -m venv "venv"
.\venv\Scripts\activate

# For Ubuntu 20.04 Bash
python3.9.5 -m install virtualenv
python3.9.5 -m virtualenv venv
chmod +x ./venv/bin/activate
source ./venv/bin/activate
```

Requirements:

* **Python** version ``3.9.5`
* **requests** version ``2.28.1`
* **beautifulsoup4** version ``4.11.1`
* **openpyxl** version ``3.0.10`
* **XlsxWriter** version ``3.0.3`
* **numpy** version ``1.23.5`
* **wget** version ``3.2`

Install dependencies while virtual environment is active:

```
# Install versions according to requirements
pip install -r requirements.txt

# or (This might cause version problems)
pip install requests beautifulsoup4 python-dateutil openpyxl xlsxwriter numpy wget
```

How to run (while virtual environment is active):

```
python main.py
```
