import functions

#Kullanıcıdan grammar ve sentences dosyaları alınır
grammar_file = input("Enter the grammar file name: ").strip()
sentence_file = input("Enter the sentence file name: ").strip()

#Grammar dosyası açılır,okunur ve dictionary oluşturulur
grammar_dict=functions.grammar_to_dict(grammar_file)

#Kelime bazlı mı yoksa karakter bazlı mı olduğu kontrol edilir
is_word_based = functions.is_word_based(grammar_dict)

#Başlangıc sembolü belirlenir
start_symbol = list(grammar_dict.keys())[0]

#Cümle dosyası açılır ve cümleler alınır
sentences = functions.get_sentences(sentence_file)

#Cümleler tokenizate edilir, kelime bazlı ise kelimelere, karakter bazlı ise karakterlere ayrılır
tokenizated_sentence=functions.tokenizate(sentences=sentences, is_word_based=is_word_based)

#################################################################################################
"""
#               Word Based function and its extra parameters

index=[0]
is_correct_sentence=[False]
parse_counter=[1]
list_for_json=[]
last_value=[]
condition = [False]

print(functions.parse_word_based(tokenizated_sentence, grammar_dict, start_symbol,index,parse_counter,is_correct_sentence,list_for_json,last_value,condition))
print(list_for_json)
"""
#################################################################################################

#================================================================================================

#################################################################################################
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
#################################################################################################

#================================================================================================

#################################################################################################
"""
#               Letter Based parsing function and its extra parameters

tokenizated_sentence = functions.tokenizate(sentences=sentences, is_word_based=is_word_based)
tokens = [t for t in tokenizated_sentence[0] if t.strip()]
list_for_json = []
final_pos = functions.parse_letter_based_v2(tokens=tokens, grammar=grammar_dict, symbol=start_symbol, pos=0, list_for_json=list_for_json)
is_correct = (final_pos == len(tokens))
print(is_correct)
print(list_for_json)

"""

