import json

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

# print(functions.tokenizate(sentences=sentences, is_word_based=is_word_based))


#Kelime bazlı mı yoksa karakter bazlı mı olduğunu kontrol edilir

#################################################################################################
"""
#               Word Based function and its extra parameters

tokenizated_sentence=functions.tokenizate(sentences=sentences, is_word_based=is_word_based)
index=[0]
is_correct_sentence=[False]
parse_counter=[1]
list_for_json=[]
last_value=[]
condition = [False]

print(functions.parse_word_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammer_dict, start_symbol=start_symbol,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json,last_value=last_value,condition=condition))
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

print(functions.parse_letter_based(tokenizated_sentence=tokenizated_sentence, grammar_dict=grammer_dict, start_symbol=start_symbol,index=index,parse_counter=parse_counter,is_correct_sentence=is_correct_sentence,list_for_json=list_for_json))
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
final_pos = functions.parse_letter_based_v2(tokens=tokens, grammar=grammer_dict, symbol=start_symbol, pos=0, list_for_json=list_for_json)
is_correct = (final_pos == len(tokens))
print(is_correct)
print(list_for_json)

"""



# # Test 1: Epsilon grammar, YANLIŞ cümle
# letter_dict = {"S": [['A', 'B']], "A": [['a', 'A'], ['ε']], "B": [['b', 'B'], ['ε']]}
# tokens = ['a', 'a', 'b', 'b', 'a', 'a']
# list_for_json = []
# final_pos = functions.parse_letter_based_v2(tokens=tokens, grammar=letter_dict, symbol='S', pos=0, list_for_json=list_for_json)
# print(final_pos == len(tokens))
# print(list_for_json)

# # Test 2: Epsilon yok, YANLIŞ cümle  
# letter_dict2 = {"S": [['A', 'B']], "A": [['a', 'A'], ['a']], "B": [['b', 'B'], ['b', 'b']]}
# tokens2 = ['a', 'a', 'b', 'c']
# list_for_json2 = []
# final_pos2 = functions.parse_letter_based_v2(tokens=tokens2, grammar=letter_dict2, symbol='S', pos=0, list_for_json=list_for_json2)
# print(final_pos2 == len(tokens2))
# print(list_for_json2)



# # Test 3: Epsilon grammar, DOĞRU cümle
# tokens = ['a', 'a', 'b', 'b']
# list_for_json = []
# final_pos = functions.parse_letter_based_v2(tokens=tokens, grammar=letter_dict, symbol='S', pos=0, list_for_json=list_for_json)
# print(final_pos == len(tokens))
# print(list_for_json)

# # Test 4: Epsilon yok, DOĞRU cümle
# tokens2 = ['a', 'a', 'b', 'b']
# list_for_json2 = []
# final_pos2 = functions.parse_letter_based_v2(tokens=tokens2, grammar=letter_dict2, symbol='S', pos=0, list_for_json=list_for_json2)
# print(final_pos2 == len(tokens2))
# print(list_for_json2)

# list1= [['S', ['A', 'B']], ['A', ['a', 'A']], ['A', ['a', 'A']], ['A', ['ε']], ['B', ['b', 'B']], ['B', ['b', 'B']], ['B', ['ε']]]

# result = functions.generate_json_from_list_letter(list1)

# print(result)

# tree_dict = json.loads(result)
# print(functions.print_parse_tree(tree_dict))
    

