# Logs Analysis Project
Analyze logs of a blog site.

This project is part of the Udacity Full Stack Nano Degree Program

## Setup
You'll need to create the database and populate it with data (you can get the `newsdata.sql` file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip it and place it inside the repository folder). You need to do this once:
```
# clone the repository
$ git clone https://github.com/sarmadmjg/logs-analysis-project
$ cd logs-analysis-project

# Create the news database
$ psql -c 'create database news'

# Connect and populate the db
$ psql -d news -f newsdata.sql
```

## Usage
```
$ python3 analyze.py
```
To save the report to a file, use this instead:
```
$ python3 analyze.py > report.txt
```
