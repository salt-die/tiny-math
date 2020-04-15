def table_maker(*rows):
    """Generates an aligned table. Modified from https://github.com/salt-die/Table-Maker"""
    rows = list(rows)

    # Pad the length of items in each column
    lengths = tuple(map(len, rows[0]))
    for i, row in enumerate(rows):
        for j, (item, length) in enumerate(zip(row, lengths)):
            rows[i][j] = f'{item:^{length}}'

    # Make separators
    horizontals = tuple("─" * (length + 2) for length in lengths)
    top, title, bottom = (f'{l}{m.join(horizontals)}{r}' for l, m, r in ('┌┬┐', '├┼┤', '└┴┘'))

    table = [f'│ {" │ ".join(row)} │' for row in rows]
    table.insert(0, top)
    table.insert(2, title)
    table.append(bottom)
    table = '\n'.join(table)
    return table