import string

def is_valid(str):

    retval=True
    min_pw_len = 3
    max_pw_len = 20

    if not min_pw_len <= len(str) <= max_pw_len:
        retval = False
    else:
        for chr in str:
            if chr not in string.ascii_letters and chr not in string.digits:
                retval = False

    return retval