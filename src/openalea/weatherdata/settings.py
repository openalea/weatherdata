from pathlib import Path

PATH_CACHE = Path.home()/'weatherdata'/'cache'

def create_dir(path):
    if not path.exists():
        create_dir(path.parent)
        path.mkdir()
    else:
        pass

def pathCache(path=None):
    '''
    Create pathCache directory
    '''
    if path==None:
        path=PATH_CACHE

    create_dir(path)
    return path

