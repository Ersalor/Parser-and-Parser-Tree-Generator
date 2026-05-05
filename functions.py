def grammar_to_dict(grammar_file):

    with open(grammar_file, 'r', encoding='utf-8') as file:
        lines=file.readlines()

#Grammer dosyasından dictionary oluşturulur
    grammar = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue   
        left, right = line.split(' ::= ')
        left = left.strip()
        right = right.strip()
        right_parts = [part.strip() for part in right.split('|')]
        for part in right_parts:
            right_parts[right_parts.index(part)] = part.split(" ")

        if ["ε"] in right_parts:
            right_parts.remove(["ε"])
            right_parts.append(["ε"])
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

def get_sentences(sentence_file):
    with open(sentence_file, 'r', encoding='utf-8') as file:
        sentences = [sentence.strip() for sentence in file.readlines()]
    return sentences

def tokenizate(*,sentences, is_word_based):
    tokenizated_sentences = []
    for sentence in sentences:
        if is_word_based:
            tokenizated_sentences.append(sentence.split())
        else:
            tokenizated_sentences.append(list(sentence))
            tokenizated_sentences[0].append(" ")

    if len(sentences) == 0:
        tokenizated_sentences.append(" ")
   
    return tokenizated_sentences

def parse(*, tokens, grammar, symbol, pos, list_for_json):
    if symbol not in grammar:
        # Terminal - sadece değeri döndür, listeye ekleme (parent ekliyor)
        if symbol == 'ε':
            return pos
        if pos < len(tokens) and tokens[pos] == symbol:
            return pos + 1
        return None

    for production in grammar[symbol]:
        current_pos = pos
        success = True
        temp_json = []

        # Eğer production tek elemanlı terminal ise: ['<determiner>', 'a'] formatında ekle
        # Eğer non-terminal içeriyorsa: ['<noun-phrase>', ['<determiner>', '<noun>']] formatında ekle
        all_terminals = all(item not in grammar and item != 'ε' for item in production)
        
        if all_terminals and len(production) == 1:
            # Terminal production: ['<verb>', 'admired'] gibi
            item = production[0]
            if pos < len(tokens) and tokens[pos] == item:
                list_for_json.append([symbol, item])
                return pos + 1
            return None
        else:
            temp_json.append([symbol, production])

        for item in production:
            if item == 'ε':
                continue
            result = parse(
                tokens=tokens,
                grammar=grammar,
                symbol=item,
                pos=current_pos,
                list_for_json=temp_json
            )
            if result is None:
                success = False
                break
            current_pos = result

        if success:
            list_for_json.extend(temp_json)
            return current_pos

    return None


#           1) 5 terminalli bir value değerinde arama yaparken mesela 3. de bulduğunda 4 v4 5. leri kontrol etmememli.Bunu ayarla.
#           2) Terminal counter'ın yeri değişti(doğruluğunu kontrol et)
#           3) <verb-phrase> ::= <verb> | <verb> <noun-phrase> olduğunda ilk <verb> eşleştiğinde cümlede başka kelime yoksa ve 
#             aranan terminalle eşleşiyorsa bitsin.Ama a man saw the dog da mesela saw dan sonra the dog var.Bu yüden sadece <verb>
#             yetmez diye düşünüp <verb> <noun-phrase> denemeye başlamalı.
#           4) Grammer de dolaşarak cümle sağlanabildiyse cümle eleman sayısı = index[0] olduysa cümle yazılabiliyor dicez.
#              Çünkü her uygun deneme yapıldığında index[0] artıyor ve cümle eleman sayısına eşit olduğunda(hatasız arama yaparak)
#              cümleyi başarıyla oluşturabilmişiz demektir.