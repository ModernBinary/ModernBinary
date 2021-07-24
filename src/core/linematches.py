BASE = {
    '112': {'c': 'print', 'argsfrommatches': ['1'], 'argvs':[], 'kwargs':{'end': '""'}}
}

def get(code):
    for c, v in BASE.items():
        if str(c) == str(code):
            return v
    return None