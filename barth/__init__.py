

def get_location(row):
    try:
        return int(row['loc'].split('.')[2])
    except:
        print('ERROR: {}'.format(type(row)))
        raise


def is_before_election(row):
    loc = get_location(row)
    return loc < 33


def is_election(row):
    loc = get_location(row)
    return loc == 33


def is_after_election(row):
    loc = get_location(row)
    return loc > 33
