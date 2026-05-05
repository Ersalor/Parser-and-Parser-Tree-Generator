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
tokenizated_sentence = functions.tokenizate(sentences=sentences, is_word_based=is_word_based)
tokens = [t for t in tokenizated_sentence[0] if t.strip()]
list_for_json = []
final_pos = functions.parse(tokens=tokens, grammar=grammer_dict, symbol=start_symbol, pos=0, list_for_json=list_for_json)
is_correct = (final_pos == len(tokens))
print(is_correct)
print(list_for_json)