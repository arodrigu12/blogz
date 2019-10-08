import hashlib, random, string

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()

    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)

def check_pw_hash(password, hash):
    salt = hash.split(',')[1]

    if make_pw_hash(password, salt) == hash:
        return True
    
    return False

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