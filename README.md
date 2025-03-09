### Hexlet tests and linter status:
[![Actions Status](https://github.com/lovedr6s/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lovedr6s/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/8eadce3bb95a371cf1b7/maintainability)](https://codeclimate.com/github/lovedr6s/python-project-83/maintainability)

# Page analyser
### App for analyse web pages. The application checks the aviability of websites and getting their headers, descriptions and H1 tags.

## Features
* URL aviability check
* Analysis of title and description tag
* Display check results on the user interface

## Demo
### You can view application on the website: [Page Analyzer](https://python-project-83-1xm8.onrender.com)

## Libraries:
* flask
* bs4
* flake8
* gunicorn
* psycopg2
* pytest
* python-dotenv
* requests
* validators

## Installation and Running
Use the `Makefile` to install and run the program
```bash
git clone https://github.com/lovedr6s/python-project-83.git
cd python-project-83

## Configuration
Before running make .env file with:
- 'SECRET_KEY': a secret key. can be anything
- 'DATABASE_URL': your link to your database
### Example
SECRET_KEY = 'meow'
DATABASE_URL = 'sql://oof'

## Install dependies
make install

## Run the local development server
make dev

## Run the production server
make start
```

## Program asciinema
[![asciicast](https://asciinema.org/a/F5SyXaq0SW2NavdzGMSEbUSQZ.svg)](https://asciinema.org/a/F5SyXaq0SW2NavdzGMSEbUSQZ)