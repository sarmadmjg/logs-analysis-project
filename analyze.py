#!/usr/bin/env python3
"""
Analyze the visiting logs of a blog
A project for the Udacity Full Stack Nano Degree Program
"""

import psycopg2
import setupdb
from logs_printer import print_table


def top_articles(cur, lim=-1):
    """analyze the most visited articles

    Args:
        cur (cursor): a cursor connected to the news database
        lim (int, optional): the max number of returned articles,
                             negative numbers mean return all

    Returns:
        (headers, result):
            headers (tuple): Common header names
            result (list): The most visited articles (as tuples)
                           sorted by views in desc order
    """
    query = """
        select article_title, count(*) as views from linkedlog
            group by article_title
            order by views desc
            {}
        """.format('limit ' + str(lim) if lim >= 0 else '')

    cur.execute(query)
    headers = ('Article', 'Views')
    return (headers, cur.fetchall())


def top_authors(cur, lim = -1):
    """analyze the most popular authors by article visits

    Args:
        cur (cursor): a cursor connected to the news database
        lim (int, optional): the max number of returned articles, negative numbers mean return all

    Returns:
        list: a list of the top authors, sorted by popularity in desc order
    """
    query = """
        select author_id, author_name, count(*) as visits from linkedlog
            group by author_name, author_id
            order by visits desc
            {}
        """.format('limit ' + str(lim) if lim >= 0 else '')

    cur.execute(query)
    headers = ('Author\'s ID', 'Author\'s Name', 'Views')
    return (headers, cur.fetchall())


def days_high_error(cur, ratio = 0.01, lim = -1):
    """Identify the days with high error ratios

    Args:
        cur (cursor): a cursor connected to the news database
        ratio (float, optional): between 0.0 and 1.0, the minimum ratio of errors/total requests
        lim (int, optional): the max number of returned articles, negative numbers mean return all

    Returns:
        list: a list of the days with high error ratio, sorted by percentage of errors in desc order
    """

    # A few remarks on this query:
    # 1---  casting the first count to float is necesary bc
    #       psql doesn't cast automatically when dividing integers
    # 2---  having is evaluated before the aggregations, so
    #       we can't use the alias (e_ratio) in having.
    query = """
        select date(time) as day,
            count(*) filter (where status >= '400')::float / count(*) as e_ratio
            from log
            group by day
            having (count(*) filter (where status >= '400')::float / count(*)) > {0}
            order by day
            {1}
        """.format(ratio, 'limit ' + str(lim) if lim >= 0 else '')

    cur.execute(query)
    headers = ('Date', 'Error Ratio')
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

    # <---------------- Logs ---------------->
    # Top articles
    num = 3
    title = 'Top Articles of All Time'
    report = top_articles(cur, num)
    print_table(*report, title)

    # Top authors
    num = 3
    title = 'Top Authors of All Time'
    report = top_authors(cur, num)
    print_table(*report, title)

    # Bad days
    threashold = 0.01
    num = -1
    title = 'Days with High Ratio of Errors'
    report = days_high_error(cur, threashold, num)
    print_table(*report, title)

    # Close the connection to db
    db.close()



if __name__ == '__main__':
    main()
