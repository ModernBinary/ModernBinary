OPERATORS = [
    '==',
    '!=',
    '>=',
    '<=',
    '<',
    '>'
]

BASE = {
    '112': {
        'c': 'print',
        'argvs':[],
        'kwargs':{
            'end': '""'
            }
        },
    '105': {
        'c': 'input',
        'argvs':[],
        'kwargs':{}
        }
}

def get(code):
    for c, v in BASE.items():
        if str(c) == str(code):
            return v
    return None