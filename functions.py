def grammar_to_dict(grammar_file):

    with open(grammar_file, 'r', encoding='utf-8') as file:
        lines=file.readlines()

#Grammer dosyasından dictionary oluşturulur
    grammar = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue   
        left, right = line.split('::=')
        left = left.strip()
        right = right.strip()
        right_parts = [part.strip() for part in right.split('|')]
        for part in right_parts:
            right_parts[right_parts.index(part)] = part.split(" ")
        grammar[left] = right_parts

    # #Grammer dosyasından üretilen dictionary yazdırılır
    # print("Grammar Dictionary: \n")
    # for key, value in grammar.items():
    #     print(f"{key} ::= {value}")

    return grammar

def is_word_based(grammar_dict):

    terminals = []
    values = list(grammar_dict.values())
    for value in values:
        for part in value:
            if len(part) == 1:
                if part[0] in grammar_dict:
                    continue
                else:
                    terminals.append(part[0])
            else:
                for item in part:
                    if item in grammar_dict:
                        continue
                    else:
                        terminals.append(item)
    for terminal in terminals:
        if len(terminal) > 1:
            return True
    return False

