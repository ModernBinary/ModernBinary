def tomb(text):
    if not text:
        return
    base = [ord(i) for i in text]
    base2 = [j*(i+1) for i, j in enumerate(base)]
    return ' '.join([str(i) for i in base2])

def totext(text):
    if not text:
        return
    text = text.split(' ')
    base = [int(int(j)/(index+1)) for index, j in enumerate(text)]
    return ''.join([chr(i) for i in base])