import json

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
        
        if ["ε"] in right_parts:
            right_parts.remove(["ε"])
            right_parts.append(["ε"])

        grammar[left] = right_parts

    # #Grammer dosyasından üretilen dictionary yazdırılır
    # print("Grammar Dictionary: \n")
    # for key, value in grammar.items():
    #     print(f"{key} ::= {value}")

    return grammar

##########################################################################################################

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

##########################################################################################################

def get_sentences(sentence_file):
    with open(sentence_file, 'r', encoding='utf-8') as file:
        sentences = [sentence.strip() for sentence in file.readlines()]
    return sentences

##########################################################################################################

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

##########################################################################################################

def parse_word_based(*,tokenizated_sentence, grammar_dict, start_symbol,index=None,parse_counter=None,is_correct_sentence=None,list_for_json=None,last_value=None,condition=None):
    
    if start_symbol not in grammar_dict:
        print(f"Error: {start_symbol} is not a non-terminal symbol in the grammar.")
        return False
    else:
        exit_loops=False
        is_correct_word_found = False
        terminal_counter = 0
        for value in grammar_dict[start_symbol]:
            write_json = True ###
            for item in value:

                if item in grammar_dict:
                    
                    if parse_counter[0] == 0:
                        break

                    parse_counter[0] += 1
                    
                    if write_json:
                        list_for_json.append( [start_symbol, value])
                        write_json = False
                    last_value.append(grammar_dict[start_symbol]) 
                    parse_word_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json,last_value=last_value,condition=condition)
                    if last_value: 
                        last_value.pop()
                    if parse_counter[0] != 0:
                        parse_counter[0] -= 1

                else:
                    terminal_counter +=1

                    if item == tokenizated_sentence[0][index[0]]:
                        index[0] +=1
                        list_for_json.append( [start_symbol, item])
                        is_correct_word_found = True
                        exit_loops=True

                        if index[0] == len(tokenizated_sentence[0]):
                            is_correct_sentence[0] = True
                            parse_counter[0] = 0
                            
                        break
        
                    else:
                        if len(grammar_dict[start_symbol]) == terminal_counter and not is_correct_word_found: #Eğer value içinde terminal sayısı kadar terminal kontrolü yapıldıysa ve hiçbiri eşleşmediyse hata verilir.
                            ##############################################################################
                            if [start_symbol] != last_value[-1][-1]:
                                print("Çalıştı")
                                exit_loops=True
                                condition[0] = True
                                break
                            ##############################################################################
                            else:
                                if index[0]-1 < 0: #index negatif olucaksa sentence hatalıdır deyip uyarı verilcek....
                                    #hata
                                    print("Error: The sentence cannot be generated by the grammar.")
                                    parse_counter[0] = 0
                                    return False
                                else:
                                    index[0] -=1 #terminal eşleşmediği için index geri alınır ve diğer alternatifler denenir.
                                    list_for_json.pop() #Eğer value içindeki terminallerden hiçbiri eşleşmediyse list_for_json dan da son eklenen item silinir.
                                    #Burda sadece value değeri silindiği için 1 tane pop var.Terminal de yazdırılmış olsaydı 2 pop atacaktık(ki onu başka if bloğunda yapıyoruz). 

                #if item == value[-1] and value == grammar_dict[start_symbol] and item not in grammar_dict and index[0] != len(tokenizated_sentence[0])-1:
                #   index[0] -=1 #Eğer value terminaller arasındaki son elemansa ve cümledeki kelime sayısı ile index eşit değilse demekki bu value ile cümle oluşturulamaz ve index geri alınır.
                if value != grammar_dict[start_symbol][-1] and item in grammar_dict and index[0] != len(tokenizated_sentence[0])-1 and not is_correct_sentence[0]:
                    if condition[0]: 
                        list_for_json.pop() 
                        continue

                    else:
                        index[0] -=1
                        list_for_json.pop() 
                        list_for_json.pop() #Eğer value içindeki item non-terminal ise ve value içindeki son item değilse ve cümledeki kelime sayısı ile index eşit değilse demekki bu value ile cümle oluşturulamaz ve index geri alınır. Aynı zamanda list_for_json dan da son eklenen item silinir.
                
            if exit_loops:
                break

    return is_correct_sentence[0]

##########################################################################################################

# Hatalı parse fonksiyonu
def parse_letter_based(*,tokenizated_sentence, grammar_dict, start_symbol,index=None,parse_counter=None,is_correct_sentence=None,list_for_json=None):
    

    if start_symbol not in grammar_dict:
        print(f"Error: {start_symbol} is not a non-terminal symbol in the grammar.")
        return False
    else:
        pass_value = False
        exit_loops=False
        is_correct_word_found = False
        terminal_counter = 0
        for value in grammar_dict[start_symbol]:
            ##############################################################################
            write_json = True ###
            ##############################################################################
            for item in value:
                if item == "ε":
                    if item == value[-1] and index[0] != len(tokenizated_sentence[0])-1 : #Epsilon son elemansa 
                        pass_value = True
                        if list_for_json[-1] != [start_symbol, item]: 
                            list_for_json.append([start_symbol, item])                                                 # aa lardan bb lere geçerken pass etmemizi sağlıyor
                        break                                                              # eğer cümlenin sonuncu kelimesi değilse çalıştırır
                                                                                           # Son elemansa aşağıda zaten kontrol ediyoruz...
                    # else:         #Ortadaki epsilonlar için dictionary ye çevirirken sona atma yapılabilir. 
                    #     continue

                if item in grammar_dict:
                    parse_counter[0] += 1
                    ##############################################################################
                    if write_json:
                        list_for_json.append( [start_symbol, value])
                        write_json = False
                    ##############################################################################
                    parse_letter_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json)
                    parse_counter[0] -= 1
                    if parse_letter_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json) == 0 and parse_counter[0] != 1: #Eğer item "ε" ise ve value içindeki son item değilse diğer alternatifler denenir.
                        return 0
                        
                else:
                    terminal_counter +=1
                        
                    if index[0] == len(tokenizated_sentence[0])-1:
                        if item == "ε":
                            pass_value = True
                            # print("Correct sentence")
                            is_correct_sentence[0] = True
                            if list_for_json[-1] != [start_symbol, item]: 
                                list_for_json.append([start_symbol, item])
                            break
                    #son karakter problemi çözülecek

                    if item == tokenizated_sentence[0][index[0]]:
                        index[0] +=1
                        is_correct_word_found = True
                        if len(value) == 1:
                            exit_loops=True
                            break
                    # if item == "ε" and index[0] == len(tokenizated_sentence) -1:
                    #     print("Doğru cümle")
                    #     return 0

                    else:
                        if len(grammar_dict[start_symbol]) == terminal_counter and not is_correct_word_found: #Eğer value içinde terminal sayısı kadar terminal kontrolü yapıldıysa ve hiçbiri eşleşmediyse hata verilir.
                            if index[0]-1 < 0: #index negatif olucaksa sentence hatalıdır deyip uyarı verilcek....
                                #hata
                                print("Error: The sentence cannot be generated by the grammar.")
                            else:
                                index[0] -=1 #terminal eşleşmediği için index geri alınır ve diğer alternatifler denenir.
                        else:
                            pass_value = True
                            break

                    
                #if item == value[-1] and value == grammar_dict[start_symbol] and item not in grammar_dict and index[0] != len(tokenizated_sentence[0])-1:
                #   index[0] -=1 #Eğer value terminaller arasındaki son elemansa ve cümledeki kelime sayısı ile index eşit değilse demekki bu value ile cümle oluşturulamaz ve index geri alınır.
                if value != grammar_dict[start_symbol][-1] and item in grammar_dict and index[0] != len(tokenizated_sentence[0])-1:
                    index[0] -=1

            if pass_value:
                if item == "ε" :
                    return 0
                
                continue 
            
            if exit_loops:
                break

    return is_correct_sentence[0]

##########################################################################################################

def parse_letter_based_v2(*, tokens, grammar, symbol, pos, list_for_json):
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
            result = parse_letter_based_v2(
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

##########################################################################################################

# Word Based grammar için JSON Formatına çevirme Fonksiyonu
def generate_json_from_list_word(list_for_json):
    # Listeyi bir yineleyiciye (iterator) çeviriyoruz. 
    # Böylece next() ile elemanları sırayla tek tek yutacağız.
    iterator = iter(list_for_json)

    def build_tree():
        try:
            # Sıradaki düğümü al (Örn: ['<noun>', 'man'])
            node = next(iterator)
        except StopIteration:
            return None, None

        # Proje gereksinimi: '<' ve '>' işaretlerini temizle
        raw_key = node[0]
        key = raw_key.replace("<", "").replace(">", "")
        value = node[1]

        # 1. Terminal Durumu: Eğer value bir string ise (Örn: 'man'), en alt daldıyız.
        if isinstance(value, str):
            return key, value

        # 2. Non-Terminal Durumu: Eğer value bir listeyse (Örn: ['<determiner>', '<noun>']), alt dallar vardır.
        children_dict = {}
        
        # 'value' listesinde kaç tane alt eleman varsa, ağaçtan o kadar parça koparmamız gerekiyor.
        for _ in range(len(value)):
            child_key, child_val = build_tree()
            if child_key:
                children_dict[child_key] = child_val

        return key, children_dict

    # Özyinelemeli inşa sürecini başlat
    root_key, root_tree = build_tree()

    # En dıştaki ana Sözlüğü (Dictionary) oluştur
    final_dict = {root_key: root_tree}
    
    # Python Sözlüğünü, girintili (indent=4) ve okunabilir bir JSON stringine çevir
    return json.dumps(final_dict, indent=4, ensure_ascii=False)

##########################################################################################################

# Letter Based grammar için JSON Formatına çevirme Fonksiyonu
def generate_json_from_list_letter(list_for_json):
    if not list_for_json:
        return "{}"

    # 1. Non-Terminal (Kural) Tespiti:
    # Listenin sol tarafındaki her şey kuraldır ('S', 'A', 'B'). 
    # Bunları bir kümeye alıyoruz ki terminal/non-terminal ayrımını sistem kendi anlasın.
    non_terminals = set([item[0] for item in list_for_json])
    
    # 2. Listeyi yineleyiciye (stream) çeviriyoruz.
    iterator = iter(list_for_json)

    def build_tree(symbol):
        # Eğer gelen sembol bir kural değilse (yani 'a', 'b' veya 'ε' gibi bir terminalse)
        # Listeden hiçbir şey ÇEKME! Doğrudan sembolün kendisini yaprak (leaf) olarak dön.
        if symbol not in non_terminals:
            return symbol
        
        # Eğer sembol bir kural ise, listeden sıradaki açılımı çek (Tüketim)
        try:
            node = next(iterator)
        except StopIteration:
            return None
        
        rhs = node[1] # Sağ taraf (Örn: ['a', 'A'] veya sadece 'b')
        
        # Eğer sağ taraf sadece düz bir string ise (Listenin sonundaki ['B', 'b'] durumu)
        # Üzerinde döngü kurabilmek için onu listeye çeviriyoruz.
        if isinstance(rhs, str):
            rhs = [rhs]

        children_dict = {}
        # Kuralın sağ tarafındaki her bir parça için özyinelemeli (recursive) olarak dallan
        for child in rhs:
            child_val = build_tree(child)
            # Json anahtarlarını oluştur (Gramer 1 için < > temizliği, Gramer 2'yi bozmaz)
            clean_child = child.replace("<", "").replace(">", "")
            children_dict[clean_child] = child_val
        
        return children_dict

    # Motoru ilk kural ile (Listenin en başındaki S) ateşle
    root_symbol = list_for_json[0][0]
    root_tree = build_tree(root_symbol)

    # En dıştaki sözlüğü (JSON objesini) oluştur
    final_dict = {root_symbol.replace("<", "").replace(">", ""): root_tree}
    
    # İnsan tarafından okunabilir formata dönüştür
    return json.dumps(final_dict, indent=4, ensure_ascii=False)

##########################################################################################################

#Parse Tree Yazdırma Fonksiyonu
#-Elde ettiğimiz JSON formatının dictionary formunu girdi olarak alır
# tree_dict=json.loads(json_string) 
def print_parse_tree(tree_dict, indent=""):
    # Sözlükteki elemanları (dalları) sırayla geziyoruz
    items = list(tree_dict.items())
    
    for i, (key, value) in enumerate(items):
        is_last = (i == len(items) - 1)
        # Son elemansa "└──", değilse "├──" kullanıyoruz
        prefix = "└── " if is_last else "├── "
        
        # Düğümün kendisini (Non-Terminal veya Terminal kuralı) yazdır
        print(indent + prefix + str(key))
        
        # Eğer bu düğümün altında başka dallar (sözlük) varsa, içeri doğru özyinelemeli dal
        if isinstance(value, dict):
            # Alt dallar için girintiyi (indentation) ayarla
            extension = "    " if is_last else "│   "
            print_parse_tree(value, indent + extension)
            
        # Eğer bu düğümün değeri düz bir metinse (Uçbirim/Terminal ise), onu da yaprak olarak yazdır
        elif isinstance(value, str):
            extension = "    " if is_last else "│   "
            # Kelimeyi [ "kelime" ] formatında belirginleştir
            print(indent + extension + "└── [ \"" + value + "\" ]")

##########################################################################################################

# Hatalı çıkan cümleler için hata mesajı yazdırma fonksiyonu yazılacak...