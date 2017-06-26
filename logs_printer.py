"""Print data in tabulated form
"""


def print_table(headers, rows, title):
    """Print query results with headers

    Args:
        headers (tuple): Headers of the table
        rows (list): a list of tuples, represent entries in table
        title (str): A title for the table
    """
    vert_sep = '|'
    hor_sep = '-'
    col_padding = 2

    print()
    print(title)
    print()

    # Calculate the optimal width for each column based on the headers and data
    # These can probably fit in one line, but this is easier to debug

    # Find widths of headers
    header_widths = [len(x) for x in headers]

    ln = len(headers)

    # Find max width of each column
    rows_widths = []
    for i in range(ln):
        rows_widths.append(max([len(str(rows[x][i]))
                                for x in range(len(rows))]))

    # Choose the max width for each col from the header and rows, add padding
    col_widths = [max(header_widths[i],
                      rows_widths[i]) + col_padding for i in range(ln)]

    # Construct a horizontal ruler
    hor_line = vert_sep.join([hor_sep * col_widths[i] for i in range(ln)])

    # Construct the headers
    headers_str = vert_sep.join(
                    ['{:^{width}}'.format(headers[i], width=col_widths[i])
                     for i in range(ln)])

    print(hor_line)
    print(headers_str)
    print(hor_line)

    # Construnt and print the rows
    for row in rows:
        row_str = vert_sep.join(
                    ['{:<{width}}'.format(str(row[i]), width=col_widths[i])
                     for i in range(ln)])
        print(row_str)

    print(hor_line)
    print()
