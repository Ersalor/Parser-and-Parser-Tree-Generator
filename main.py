import functions
#Kullanıcıdan grammer dosyası alınır
grammar_file = "grammar2.txt" #input("Enter the grammar file name: ").strip()

#Dosya açılır,okunur ve dictionary oluşturulur
grammer_dict=functions.grammar_to_dict(grammar_file)

#Kelime bazlı mı yoksa karakter bazlı mı olduğu kontrol edilir
is_word_based = functions.is_word_based(grammer_dict)
start_symbol = list(grammer_dict.keys())[0]

#Kullanıcıdan cümle dosyası alınır
sentence_file = "sentence2.txt" #input("Enter the sentence file name: ").strip()

#Cümle dosyası açılır ve cümleler alınır
sentences = functions.get_sentences(sentence_file)

print(functions.tokenizate(sentences=sentences, is_word_based=is_word_based))


#Kelime bazlı mı yoksa karakter bazlı mı olduğunu kontrol edilir
tokenizated_sentence=functions.tokenizate(sentences=sentences, is_word_based=is_word_based)
index=[0]
is_correct_sentence=[False]
parse_counter=[1]
list_for_json=[]
last_value=[]
condition = [False]

#print(functions.parse_word_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammer_dict, start_symbol=start_symbol,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json,last_value=last_value,condition=condition))
print(functions.parse_letter_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammer_dict, start_symbol=start_symbol,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json))
print(list_for_json)

#Verb2 problemi çözülmedi
