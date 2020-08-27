import os


def is_path_correct(p):
    if os.path.exists(p):
        return p
    else:
        raise Exception(p)