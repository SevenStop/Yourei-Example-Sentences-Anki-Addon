from .collectData import data

def get_sentence(word = '検査'):
    received = data(word,0)

    #html processing
    processed = []
    for line in received:
        print(line)
        # remove newline chars
        one_line_string = line.replace("\n", "")
        print(one_line_string)
        #add formatting for target word
        ins = one_line_string.replace(word, f'<span style="color:red; background-color:yellow;">{word}</span>')
        print(ins)
        #make bold
        ins = ins.replace(ins, f'<b>{ins}</b>')
        print(ins)
        processed.append(ins)

    return processed

def get_next_page(word = '検査'):
    received = data(word,)

    #html processing
    processed = []
    for line in received:
        print(line)
        # remove newline chars
        one_line_string = line.replace("\n", "")
        print(one_line_string)
        #add formatting for target word
        ins = one_line_string.replace(word, f'<span style="color:red; background-color:yellow;">{word}</span>')
        print(ins)
        #make bold
        ins = ins.replace(ins, f'<b>{ins}</b>')
        print(ins)
        processed.append(ins)

    return processed