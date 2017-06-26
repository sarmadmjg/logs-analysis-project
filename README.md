# Log Analysis Project
Analyze logs of a blog site.

This project is part of the Udacity Full Stack Nano Degree Program

## Usage
```
git clone https://github.com/sarmadmjg/logs-analysis-project
cd logs-analysis-project
python3 analyze.py
```
To save the report to a file, use this instead of the third line: `python3 analyze.py > log.txt`

Please note that this will only work on machines with a populated database according to the project requirements.

## Views
One view is created automatically in the script, you don't need to run the query manually. The query string is located in the setupdb.py file
```
create or replace view linkedlog as
        select  log.*,
                articles.id as article_id,
                articles.title as article_title,
                authors.id as author_id,
                authors.name as author_name
        from log, articles, authors
        where log.path like ('/article/' || articles.slug || '%')
              and articles.author = authors.id;
```
