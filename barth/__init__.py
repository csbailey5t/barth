

def get_location(row):
    try:
        return tuple([int(t) for t in row['loc'].split('.')][:2])
    except:
        print('ERROR: {}'.format(type(row)))
        raise


def is_before_election(row):
    loc = get_location(row)
    return loc < (4, 1)


def is_election(row):
    loc = get_location(row)
    return loc >= (4, 1) and loc <= (4, 5)


def is_after_election(row):
    loc = get_location(row)
    return loc > (4, 5)
