#!/usr/bin/env python3
"""
Analyze the visiting logs of a blog
A project for the Udacity Full Stack Nano Degree Program
"""

import psycopg2
import setupdb
import datetime
from logs_printer import print_table


def top_articles(cur, lim=3):
    """analyze the most visited articles

    Args:
        cur (cursor): a cursor connected to the news database
        lim (int, optional): the max number of returned articles

    Returns:
        (headers, result):
            headers (tuple): Common header names
            result (list): The most visited articles (as tuples)
                           sorted by views in desc order
    """
    query = """
        select title, count(*) as views
        from log, articles
        where log.path = '/article/' || articles.slug
        group by title
        order by views desc
        limit %s
        """

    cur.execute(query, (lim,))
    headers = ('Article', 'Views')
    return (headers, cur.fetchall())


def top_authors(cur):
    """analyze the most popular authors by article visits

    Args:
        cur (cursor): a cursor connected to the news database

    Returns:
        (headers, result):
                headers (tuple): Common header names
                result (list): The top authors (as tuples)
                               sorted by views in desc order
    """
    query = """
        select authors.name, count(*) as views
        from log, articles, authors
        where log.path = '/article/' || articles.slug
            and articles.author = authors.id
        group by authors.name, authors.id
        order by views desc
        """

    cur.execute(query)
    headers = ('Author', 'Views')
    return (headers, cur.fetchall())


def days_high_error(cur, threashold=0.01):
    """Identify the days with high error ratios

    Args:
        cur (cursor): a cursor connected to the news database
        threashold (float, optional): between 0.0 and 1.0
                                 the minimum ratio of errors/total requests

    Returns:
        (headers, result):
            headers (tuple): Common header names
            result (list): a list of the days with high error ratio
    """

    # A few remarks on this query:
    # 1---  casting the first count to float is necessary bc
    #       psql doesn't cast automatically when dividing integers
    # 2---  having is evaluated before the aggregations, so
    #       we have to rewrite the functions
    query = """
        select date(time) as day,
               count(*) filter (where status >= '400')::float
                      / count(*) as e_ratio
        from log
        group by day
        having (count(*) filter (where status >= '400')::float
                    / count(*)) > %s
        order by day
        """

    cur.execute(query, (threashold,))
    headers = ('Date', 'Errors')
    return (headers, cur.fetchall())


def main():
    """The entry point of the script
    """
    # Establish connection to the database
    db = psycopg2.connect(dbname='news')
    cur = db.cursor()

    # Create all the required views and commit changes
    setupdb.setup(cur)
    db.commit()

    print('Generated on: ' + datetime.datetime.now().isoformat() + ' UTC')
    print()

    # <---------------- Logs ---------------->
    # Top articles
    num = 3
    title = 'Top Articles of All Time'
    report = top_articles(cur, num)
    print_table(*report, title)

    # Top authors
    title = 'Top Authors of All Time'
    report = top_authors(cur)
    print_table(*report, title)

    # Bad days
    threashold = 0.01
    title = 'Days with High Ratio of Errors'
    report = days_high_error(cur, threashold)
    print_table(*report, title)

    # Close the connection to db
    db.close()


if __name__ == '__main__':
    main()
