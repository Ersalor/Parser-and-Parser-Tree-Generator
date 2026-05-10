import json
import graphviz
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import os
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace') if hasattr(sys.stdout, 'reconfigure') else None

# --- Graphviz PATH (gerekirse duzenle) ---
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

##########################################################################################################

def grammar_to_dict(grammar_file):

    try:
        with open(grammar_file, 'r', encoding='utf-8') as file:
            lines=file.readlines()

    except FileNotFoundError:
        print(f"Error: File '{grammar_file}' not found.")
        return {}
    except IOError as e:
        print(f"Error: Failed to read file: {e}")
        return {}
    #Grammer dosyasından dictionary oluşturulur
    grammar = {}
    for line in lines:
        try:
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
       
        except Exception as e:
            print(f"Error: Unexpected error on line '{line}': {e}")
            continue
    # #Grammer dosyasından üretilen dictionary yazdırılır
    # print("Grammar Dictionary: \n")
    # for key, value in grammar.items():
    #     print(f"{key} : {value}")

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
    try:
        with open(sentence_file, 'r', encoding='utf-8') as file:
            sentences = [sentence.strip() for sentence in file.readlines()]
        return sentences
    except FileNotFoundError:
        print(f"Error: File '{sentence_file}' not found.")
        return []
    except IOError as e:
        print(f"Error: Failed to read file: {e}")
        return []

##########################################################################################################

def tokenizate(*,sentence, is_word_based):
    tokenizated_sentence = []
    
    if is_word_based:                                 #Hata çıkarsa buraya bak!!!
        tokenizated_sentence.append(sentence.split())
    else:
        tokenizated_sentence.append(list(sentence))
        tokenizated_sentence[0].append(" ")
    
    if len(sentence) == 0:
        tokenizated_sentence.append(" ")
            
    return tokenizated_sentence

##########################################################################################################

def parse_word_based(tokenizated_sentence, grammar_dict, start_symbol,index=None,parse_counter=None,is_correct_sentence=None,list_for_json=None,last_value=None,condition=None,temp_index=None):
    
    if start_symbol not in grammar_dict:
        #print(f"Error: {start_symbol} is not a non-terminal symbol in the grammar.")
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
                    temp_index[0] = index[0]
                    parse_word_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json,last_value=last_value,condition=condition,temp_index=temp_index)
                    if last_value: 
                        last_value.pop()
                    if parse_counter[0] != 0:
                        parse_counter[0] -= 1
                    
                    if index[0] == 0 and value == grammar_dict[start_symbol][0] and parse_counter[0] == 1:
                        return False
                    if temp_index[0] == index[0] and len(value) > 1:
                        pass_value = True
                        break

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
                                #print("Çalıştı")
                                exit_loops=True
                                condition[0] = True
                                break
                            ##############################################################################
                            else:
                                if index[0]-1 < 0: #index negatif olucaksa sentence hatalıdır deyip uyarı verilcek....
                                    #hata
                                    #print("Error: The sentence cannot be generated by the grammar.")
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
def parse_letter_based_broken(tokenizated_sentence, grammar_dict, start_symbol,index=None,parse_counter=None,is_correct_sentence=None,list_for_json=None):
    

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
                    parse_letter_based_broken(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json)
                    parse_counter[0] -= 1
                    if parse_letter_based_broken(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json) == 0 and parse_counter[0] != 1: #Eğer item "ε" ise ve value içindeki son item değilse diğer alternatifler denenir.
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

#================================================================================================
"""
#               Broken Letter Based parsing function and its extra parameters

tokenizated_sentence=functions.tokenizate(sentences=sentences, is_word_based=is_word_based)
index=[0]
is_correct_sentence=[False]
parse_counter=[1]
list_for_json=[]

print(functions.parse_letter_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=start_symbol,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json))
print(list_for_json)

"""

##########################################################################################################

def parse_letter_based(tokens, grammar, symbol, pos, list_for_json):
    if symbol not in grammar:
        if symbol == 'ε':
            return pos
        if pos < len(tokens) and tokens[pos] == symbol:
            return pos + 1
        return None

    best_temp = []
    best_pos = pos  # kaç token tüketildi

    for production in grammar[symbol]:
        current_pos = pos
        success = True
        temp_json = []

        all_terminals = all(item not in grammar and item != 'ε' for item in production)

        if all_terminals and len(production) == 1:
            item = production[0]
            if pos < len(tokens) and tokens[pos] == item:
                list_for_json.append([symbol, item])
                return pos + 1
            continue

        else:
            temp_json.append([symbol, production])

        for item in production:
            if item == 'ε':
                continue
            result = parse_letter_based(
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
        else:
            # ⚠️ sadece daha fazla token tüketen production'ı sakla
            if current_pos > best_pos:
                best_temp = temp_json
                best_pos = current_pos

    list_for_json.extend(best_temp)
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
# tree_dict=json.loads(json) 
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

## ⚠️⚠️⚠️keys = set(word_dict.keys())⚠️⚠️⚠️

def find_correct_part(list_for_json, keys):
    correct_part_list = []
    for item in list_for_json:
        right = item[1]
        values = right if isinstance(right, list) else [right]
        for v in values:
            if v not in keys:
                correct_part_list.append(v)
    return correct_part_list

##########################################################################################################

def find_where_occurs(correct_part_list, tokenized_sentence,is_word_based):
    if is_word_based:
        error_token = tokenized_sentence[0][len(correct_part_list)]
        print(f"Where the error occurs: at token {len(correct_part_list)+1} (\"{error_token}\") ")
    else:
        epsilon_counter = correct_part_list.count('ε')
        error_token = tokenized_sentence[0][len(correct_part_list)-epsilon_counter]
        print(f"Where the error occurs: at token {len(correct_part_list)+1 - epsilon_counter} (\"{error_token}\") ")

##########################################################################################################

def find_expected_values_word_based(list_for_json, grammar_dict):
    expected_values = []
    correct_part_list = find_correct_part(list_for_json, set(grammar_dict.keys()))
    #last_correct_token = correct_part_list[-1]
    
    if len(correct_part_list) > 0:
        last_correct_token = correct_part_list[-1]
        current_key = None
        current_index = None

        for item in list_for_json:
            if isinstance(item[-1], list):
                continue
            else:
                if item[-1] == last_correct_token:
                    current_key = item[0]
                    break
        if current_key is None:
            print("No expected values found.Current key is unknown.")
    
        current_index = list_for_json.index([current_key,last_correct_token])
    
        expected_key = None
        if isinstance(list_for_json[current_index+1][1], list):
            expected_key = list_for_json[current_index+1][1][0]
        else:
            expected_key = list_for_json[current_index+1][1]

    else:
        if isinstance(list_for_json[-1][-1], list):
            expected_key = list_for_json[-1][-1][0]
        else:
            expected_key = list_for_json[-1][-1]


    if expected_key in grammar_dict:
        expected_values = [ values[0] for values in grammar_dict[expected_key]]

        if len(correct_part_list) == 0:
            end_of_error_message = "to start"
        else:
            end_of_error_message = "to continue"

        if len(expected_values) > 1:
            result = " or ".join(f'"{v}"' for v in expected_values)
            print(f"What was expected: a {expected_key.strip('<>')} ({result}) " + end_of_error_message)
        else:
            print(f"What was expected: a {expected_key.strip('<>')} (\"{expected_values[0]}\") " + end_of_error_message)

##########################################################################################################

def find_expected_values_letter_based(list_for_json, grammar_dict):

    def get_terminals(key):
        values = []
        for production in grammar_dict[key]:
            first = production[0]
            if first != 'ε' and first not in grammar_dict:
                values.append(first)
            elif first in grammar_dict:
                values.extend(get_terminals(first))
        return list(dict.fromkeys(values))

    def format_result(key, values, end_msg):
        if len(values) > 1:
            result = ' or '.join(f'"{v}"' for v in values)
            print(f"What was expected: a {key} ({result}) {end_msg}")
        elif len(values) == 1:
            print(f"What was expected: a {key} (\"{values[0]}\") {end_msg}")
        else:
            print("No expected values found.")

    if not list_for_json:
        first_key = next(iter(grammar_dict))
        return format_result(first_key, get_terminals(first_key), "to start")

    last_item = list_for_json[-1]
    current_key = last_item[0]
    rhs = last_item[1]

    if rhs == ['ε'] or rhs == 'ε':
        expected_values = get_terminals(current_key)
    elif isinstance(rhs, list):
        first_element = rhs[0]
        if first_element in grammar_dict:
            current_key = first_element
            expected_values = get_terminals(first_element)
        else:
            expected_values = [first_element]
    else:
        expected_values = get_terminals(current_key)

    return format_result(current_key, expected_values, "to continue")

##########################################################################################################

def why_is_invalid(list_for_json, grammar_dict,tokenizated_sentence):
    correct_part_list = find_correct_part(list_for_json, set(grammar_dict.keys()))
    #last_correct_token = correct_part_list[-1]

    if len(correct_part_list) > 0:
        last_correct_token = correct_part_list[-1]
        current_key = None
        current_index = None

        for item in list_for_json:
            if isinstance(item[-1], list):
                continue
            else:
                if item[-1] == last_correct_token:
                    current_key = item[0]
                    break
        if current_key is None:
            print("No expected values found.Current key is unknown.")
    
        current_index = list_for_json.index([current_key,last_correct_token])
    
        expected_key = None
        if isinstance(list_for_json[current_index+1][1], list):
            expected_key = list_for_json[current_index+1][1][0]
        else:
            expected_key = list_for_json[current_index+1][1]

    else:
        if isinstance(list_for_json[-1][-1], list):
            expected_key = list_for_json[-1][-1][0]
        else:
            expected_key = list_for_json[-1][-1]

    if expected_key in grammar_dict:

        if len(correct_part_list) == 0:
            begin_continue = "begin"
        else:
            begin_continue = "continue"

        error_message=(f"Why the sentence is invalid: the sentence should {begin_continue} with a {expected_key.strip('<>')}, ")

        error_token = tokenizated_sentence[0][len(correct_part_list)]

        is_in_dict= False
        word_type = None
        for key, values in grammar_dict.items():
            for value in values:
                if error_token in value:
                    is_in_dict = True
                    word_type = key.strip('<>')
                    break
        
        if is_in_dict:
            print(error_message + (f"but \"{error_token}\" is a {word_type}."))
        else:
            print(error_message + (f"but \"{error_token}\" is not in {expected_key.strip('<>') } in the grammar."))

##########################################################################################################

#               Parse Tree Görselleştirme Fonksiyonları (Graphviz ve PIL kullanarak)

##########################################################################################################

counter = [0]

def add_nodes(dot, tree, parent_id=None):
    if isinstance(tree, dict):
        for key, value in tree.items():
            node_id = f"node_{counter[0]}"
            counter[0] += 1

            if isinstance(value, str):
                # key dugumu (non-terminal)
                dot.node(node_id, label=key, shape="ellipse",
                         style="filled", fillcolor="#D6EAF8", color="#2980B9",
                         fontname="Sans Bold", fontsize="13")
                if parent_id:
                    dot.edge(parent_id, node_id)

                # terminal yaprak dugumu
                leaf_id = f"node_{counter[0]}"
                counter[0] += 1
                dot.node(leaf_id, label=value, shape="box",
                         style="filled,rounded", fillcolor="#2980B9", color="#1A5276",
                         fontcolor="white", fontname="Sans Bold", fontsize="12")
                dot.edge(node_id, leaf_id)

            else:
                dot.node(node_id, label=key, shape="ellipse",
                         style="filled", fillcolor="#D5F5E3", color="#27AE60",
                         fontname="Sans Bold", fontsize="13")
                if parent_id:
                    dot.edge(parent_id, node_id)
                add_nodes(dot, value, parent_id=node_id)

##################################################

def json_to_image(tree_json, title="Parse Tree"):
    """JSON'dan graphviz PNG olusturur, PIL Image olarak doner (dosyaya yazmadan)."""
    counter[0] = 0

    dot = graphviz.Digraph(
        comment=title,
        graph_attr={
            "rankdir": "TB",
            "splines": "ortho",
            "nodesep": "0.5",
            "ranksep": "0.6",
            "bgcolor": "white",
            "fontname": "Sans",
            "label": title,
            "labelloc": "t",
            "fontsize": "15",
        },
        edge_attr={"color": "#555555", "arrowsize": "0.7"}
    )

    add_nodes(dot, tree_json)

    # PNG'yi bellege render et (dosyaya yazmadan)
    png_bytes = dot.pipe(format="png")
    image = Image.open(io.BytesIO(png_bytes))
    return image

##################################################

def show_trees(trees: list[dict]):

    root = tk.Tk()
    root.title("Parse Tree Viewer")
    root.geometry("900x650")
    root.configure(bg="#1e1e2e")

    header = tk.Label(root, text="Parse Tree Viewer",
                      bg="#1e1e2e", fg="#cdd6f4",
                      font=("Segoe UI", 16, "bold"), pady=10)
    header.pack()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
    style.configure("TNotebook.Tab", background="#313244", foreground="#cdd6f4",
                    font=("Segoe UI", 11), padding=[12, 6])
    style.map("TNotebook.Tab",
              background=[("selected", "#89b4fa")],
              foreground=[("selected", "#1e1e2e")])

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    for item in trees:
        title = item.get("title", "Tree")
        tree_json = item["json"]

        frame = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(frame, text=title)

        loading = tk.Label(frame, text="Render ediliyor...",
                           bg="#1e1e2e", fg="#a6adc8", font=("Segoe UI", 12))
        loading.pack(expand=True)
        root.update()

        img = json_to_image(tree_json, title=title)
        loading.destroy()

        canvas_frame = tk.Frame(frame, bg="#1e1e2e")
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        h_scroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.configure(scrollregion=(0, 0, img.width, img.height))
        canvas.image = photo  

        def on_mousewheel(event, c=canvas):
            c.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", on_mousewheel)

    root.mainloop()

##########################################################################################################

def execute_parsing_and_visualization(grammar_file, sentence_file):
    
    #Grammar dosyası açılır,okunur ve dictionary oluşturulur
    grammar_dict=grammar_to_dict(grammar_file)

    #Kelime bazlı mı yoksa karakter bazlı mı olduğu kontrol edilir
    is_grammar_word_based = is_word_based(grammar_dict)

    #Başlangıc sembolü belirlenir
    start_symbol = list(grammar_dict.keys())[0]

    #Cümle dosyası açılır ve cümleler alınır
    sentences = get_sentences(sentence_file)


    if is_grammar_word_based:
        
        list_to_show_trees = []
        for sentence in sentences:

            #Cümleler tokenizate edilir, kelime bazlı ise kelimelere, karakter bazlı ise karakterlere ayrılır
            tokenizated_sentence=tokenizate(sentence=sentence, is_word_based=is_grammar_word_based)

            index=[0]
            is_correct_sentence=[False]
            parse_counter=[1]
            list_for_json=[]
            last_value=[]
            condition = [False]
            temp_index = [0]

            result =parse_word_based(tokenizated_sentence, grammar_dict, start_symbol,index,parse_counter,is_correct_sentence,list_for_json,last_value,condition,temp_index)

            print("Sentence:", sentence)
            if result:
                print("Valid sentence\n")
                json_format = generate_json_from_list_word(list_for_json)
                list_to_show_trees.append({"title": sentence, "json": json.loads(json_format)})

                print("JSON:\n", json_format)

                #Parse Tree için listeye ekleme yaptık, en son show_trees fonksiyonuna vereceğiz.

            else:
                print("Invalid sentence\n")
                print("Error:")

                keys = set(grammar_dict.keys())
                correct_part_list = find_correct_part(list_for_json, keys)
                find_where_occurs(correct_part_list, tokenizated_sentence,is_grammar_word_based)
                find_expected_values_word_based(list_for_json, grammar_dict)
                why_is_invalid(list_for_json, grammar_dict, tokenizated_sentence)
                print()
        
        #Parse Tree Görselleştirme
        if len(list_to_show_trees) > 0:
            show_trees(list_to_show_trees) 
        
    else:
        list_to_show_trees = []
        for sentence in sentences:

            tokenizated_sentence=tokenizate(sentence=sentence, is_word_based=is_grammar_word_based)

            tokens = [t for t in tokenizated_sentence[0] if t.strip()]
            list_for_json = []
            final_pos =parse_letter_based(tokens=tokens, grammar=grammar_dict, symbol=start_symbol, pos=0, list_for_json=list_for_json)
            is_correct = (final_pos == len(tokens))

            print("Sentence:", sentence)
            if is_correct:
                print("Valid sentence\n")
                json_format = generate_json_from_list_letter(list_for_json)
                list_to_show_trees.append({"title": sentence, "json": json.loads(json_format)})

                print("JSON:\n", json_format)

            else:
                print("Invalid sentence\n")
                print("Error:")

                keys = set(grammar_dict.keys())
                correct_part_list = find_correct_part(list_for_json, keys)
                find_where_occurs(correct_part_list, tokenizated_sentence,is_grammar_word_based)
                find_expected_values_letter_based(list_for_json, grammar_dict)
                print()

        #Parse Tree Görselleştirme
        if len(list_to_show_trees) > 0:
            show_trees(list_to_show_trees)  

     