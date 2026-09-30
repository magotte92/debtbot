# debtbot

A simple bot, that draw debts, concetrate them if a deadline is present and mail them to the client.

## Requirements

- Python 3.12 or newer
- Google Chrome or Chromium, for `debts.py` and `auto_mail.py`

Selenium Manager (included with Selenium 4) downloads a ChromeDriver build that matches the installed browser. This repository no longer vendors `chromedriver.exe`.

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

`prepare.py` and `debts.py` read the client CSV from the `DB` environment variable. The file is Windows-1253 text.

`auto_mail.py` reads `mail.csv` from the working directory and uses the `URL`, `USER`, and `PWD` environment variables.

```bash
DB=/path/to/clients.csv python prepare.py
DB=/path/to/clients.csv python debts.py
URL=https://mail.example/ python auto_mail.py
```

`auto_mail.py` still expects `USER` and `PWD` to be set in the environment.

## Checks

```bash
python -m pip install -r requirements-dev.txt
ruff check .
pytest
pip-audit -r requirements.txt
```
