"""Create Views on DB that the app might require
"""

def setup(cur):
    """Add all views here

    Args:
        cur (cursor): a cursor connected to the news database
    """

    # This query creates the view if it doesn't exist, or replace it if it already exist
    # Replacing the view with each run shouldn't affect perfornamce when using PostgreSQL
    query = """
        create or replace view linkedlog as
            select log.*, articles.id as article_id, articles.title as article_title,
                authors.id as author_id, authors.name as author_name from
            log, articles, authors
            where log.path like ('/article/' || articles.slug || '%')
                and articles.author = authors.id
        """

    cur.execute(query)
