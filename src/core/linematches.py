BASE = {
    '112': {
        'c': 'print',
        'argsfrommatches': ['1'],
        'argvs':[],
        'kwargs':{
            'end': '""'
            }
        },
    '105': {
        'c': 'input',
        'argsfrommatches': ['1'],
        'argvs':[],
        'kwargs':{}
        }
}

def get(code):
    for c, v in BASE.items():
        if str(c) == str(code):
            return v
    return None