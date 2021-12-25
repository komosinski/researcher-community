def check_numeric_args(*argv):
    try:
        for arg  in argv:
            arg  = int(arg)
    except:
        return False
    return True