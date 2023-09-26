def is_number(s: str):
    """Returns True if string is a number."""
    if not isinstance(s, str):
        return False
    return s.replace(".", "", 1).replace("-", "", 1).isdigit()


def cast_to_number_if_possible(s: str):
    """casts to float if the given string is a valid number"""
    if is_number(s):
        return float(s)

    return s
