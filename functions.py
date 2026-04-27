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

def parse(*,tokenizated_sentence, grammar_dict, start_symbol,index=None,parse_counter=None,is_correct_sentence=None):
    

    if start_symbol not in grammar_dict:
        print(f"Error: {start_symbol} is not a non-terminal symbol in the grammar.")
        return False
    else:
        pass_value = False
        exit_loops=False
        is_correct_word_found = False
        terminal_counter = 0
        for value in grammar_dict[start_symbol]:
            for item in value:
                if item == "ε":
                    if item == value[-1] and index[0] != len(tokenizated_sentence[0])-1 : #Epsilon son elemansa 
                        pass_value = True                                                  # aa lardan bb lere geçerken pass etmemizi sağlıyor
                        break                                                              # eğer cümlenin sonuncu kelimesi değilse çalıştırır
                                                                                           # Son elemansa aşağıda zaten kontrol ediyoruz...
                    # else:         #Ortadaki epsilonlar için dictionary ye çevirirken sona atma yapılabilir. 
                    #     continue

                if item in grammar_dict:
                    parse_counter[0] += 1
                    parse(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence)
                    parse_counter[0] -= 1
                    if parse(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammar_dict, start_symbol=item,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence) == 0 and parse_counter[0] != 1: #Eğer item "ε" ise ve value içindeki son item değilse diğer alternatifler denenir.
                        return 0
                        
                else:
                    terminal_counter +=1
                        
                    if index[0] == len(tokenizated_sentence[0])-1:
                        if item == "ε":
                            pass_value = True
                            # print("Correct sentence")
                            is_correct_sentence[0] = True
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
        
          


#           1) 5 terminalli bir value değerinde arama yaparken mesela 3. de bulduğunda 4 v4 5. leri kontrol etmememli.Bunu ayarla.
#           2) Terminal counter'ın yeri değişti(doğruluğunu kontrol et)
#           3) <verb-phrase> ::= <verb> | <verb> <noun-phrase> olduğunda ilk <verb> eşleştiğinde cümlede başka kelime yoksa ve 
#             aranan terminalle eşleşiyorsa bitsin.Ama a man saw the dog da mesela saw dan sonra the dog var.Bu yüden sadece <verb>
#             yetmez diye düşünüp <verb> <noun-phrase> denemeye başlamalı.
#           4) Grammer de dolaşarak cümle sağlanabildiyse cümle eleman sayısı = index[0] olduysa cümle yazılabiliyor dicez.
#              Çünkü her uygun deneme yapıldığında index[0] artıyor ve cümle eleman sayısına eşit olduğunda(hatasız arama yaparak)
#              cümleyi başarıyla oluşturabilmişiz demektir.