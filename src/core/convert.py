def tomb(text):
    if not text:
        return
    return ' '.join([str(i) for i in [j*(i+1) for i, j in enumerate([ord(i) for i in text.strip()])]])

def totext(text):
    if not text:
        return
    return ''.join([chr(i) for i in [int(int(j)/(index+1)) for index, j in enumerate(text.strip().split(' '))]])
