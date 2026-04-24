import functions
#Kullanıcıdan grammer dosyası alınır
grammar_file = "grammar1.txt" #input("Enter the grammar file name: ").strip()

#Dosya açılır,okunur ve dictionary oluşturulur
grammer_dict=functions.grammar_to_dict(grammar_file)

#Kelime bazlı mı yoksa karakter bazlı mı olduğu kontrol edilir
is_word_based = functions.is_word_based(grammer_dict)
start_symbol = list(grammer_dict.keys())[0]

#Kullanıcıdan cümle dosyası alınır
sentence_file = "sentence.txt" #input("Enter the sentence file name: ").strip()

#Cümle dosyası açılır ve cümleler alınır
sentences = functions.get_sentences(sentence_file)

print(functions.tokenizate(sentences=sentences, is_word_based=is_word_based))


#Kelime bazlı mı yoksa karakter bazlı mı olduğunu kontrol edilir
tokenizated_sentence=functions.tokenizate(sentences=sentences, is_word_based=is_word_based)
index=[0]
parse_counter=[1]
print(functions.parse(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammer_dict, start_symbol=start_symbol,index=index,parse_counter=parse_counter))