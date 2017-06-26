

def table_query(headers, rows):
    vert_sep = '|'
    hor_sep = '-'

    # headers = ['Real Madrid', 'Manchester United', 'Barcelona']
    # rows = [('asdf', 'asdfeeecad', 'keidniihd'),\
    #         ('ine,c', 'iencidsid asdf aasfds93', 'eac')]

    header_widths = [len(x) for x in headers]

    l = len(headers)

    rows_widths = []
    for i in range(l):
        rows_widths.append(max([len(str(rows[x][i])) for x in range(len(rows))]))

    col_widths = [max(header_widths[i], rows_widths[i]) + 2 for i in range(l)]

    hor_line = vert_sep.join([hor_sep * col_widths[i] for i in range(l)])
    headers_str = vert_sep.join(['{:^{width}}'.format(headers[i], width=col_widths[i]) for i in range(l)])

    print(hor_line)
    print(headers_str)
    print(hor_line)

    for row in rows:
        row_str = vert_sep.join(['{:<{width}}'.format(row[i], width=col_widths[i]) for i in range(l)])
        print(row_str)

    print(hor_line)
