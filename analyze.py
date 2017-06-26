#!/usr/bin/env python3
"""
Analyze the visiting logs of a blog
A project for the Udacity Full Stack Nano Degree Program

The queries are arranged in functions and called from main
to simplify switching queries on/off
"""

import psycopg2
import datetime


def top_articles(cur):
    """analyze the most visited articles

    Args:
        cur (cursor): a cursor connected to the news database
    """

    lim = 3

    query = """
        select title, count(*) as views
        from log, articles
        where log.path = '/article/' || articles.slug
        group by title
        order by views desc
        limit %s
        """

    cur.execute(query, (lim,))
    result = cur.fetchall()

    print('All-time top articles by views:')
    print('-------------------------------')
    for entry in result:
        print(entry[0] + ': ' + str(entry[1]) + ' views')
    print()


def top_authors(cur):
    """analyze the most popular authors by article visits

    Args:
        cur (cursor): a cursor connected to the news database
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
    result = cur.fetchall()

    print('All-time top authors by views:')
    print('------------------------------')
    for entry in result:
        print(entry[0] + ': ' + str(entry[1]) + ' views')
    print()


def days_high_error(cur):
    """Identify the days with high error ratios

    Args:
        cur (cursor): a cursor connected to the news database
    """

    threashold = 0.01

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
    result = cur.fetchall()

    print('Days with high error ratios:')
    print('----------------------------')
    for entry in result:
        print(entry[0].strftime("%B %d, %Y") + ': ' +
              '{0:.2f}%'.format(entry[1] * 100))
    print()


def main():
    """The entry point of the script
    """
    # Establish connection to the database
    db = psycopg2.connect(dbname='news')
    cur = db.cursor()

    print('Generated on: ' + datetime.datetime.now().isoformat() + ' UTC')
    print()

    # <---------------- Logs ---------------->
    top_articles(cur)
    top_authors(cur)
    days_high_error(cur)

    db.close()


if __name__ == '__main__':
    main()
