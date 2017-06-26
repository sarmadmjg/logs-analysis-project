#!/usr/bin/env python3
"""
Analyze the visiting logs of a blog
A project for the Udacity Full Stack Nano Degree Program
"""

import psycopg2
import setupdb


def top_articles(cur, lim = -1):
    """analyze the most visited articles

    Args:
        cur (cursor): a cursor connected to the news database
        lim (int, optional): the max number of returned articles, negative numbers mean return all

    Returns:
        list: a list of the most visited articles, sorted by popularity in desc order
    """
    query = """
        select article_title, author_name, count(*) as visits from linkedlog
            group by article_title, author_name
            order by visits desc
            {}
        """.format('limit ' + str(lim) if lim >= 0 else '')

    cur.execute(query)
    return cur.fetchall()


def top_authors(cur, lim = -1):
    """analyze the most popular authors by article visits

    Args:
        cur (cursor): a cursor connected to the news database
        lim (int, optional): the max number of returned articles, negative numbers mean return all

    Returns:
        list: a list of the top authors, sorted by popularity in desc order
    """
    pass


def days_high_error(cur, ratio = 0.01, lim = -1):
    """Identify the days with high error ratios

    Args:
        cur (cursor): a cursor connected to the news database
        ratio (float, optional): between 0.0 and 1.0, the minimum ratio of errors/total requests
        lim (int, optional): the max number of returned articles, negative numbers mean return all

    Returns:
        list: a list of the days with high error ratio, sorted by percentage of errors in desc order
    """
    pass


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
    report = top_articles(cur, 3)
    print(report)

    # Close the connection to db
    db.close()



if __name__ == '__main__':
    main()
