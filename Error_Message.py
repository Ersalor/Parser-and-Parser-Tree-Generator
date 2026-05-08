#################################################################################################
letter_dict={
    "S" : [['A', 'B']],
    "A" : [['a', 'A'], ['ε']],
    "B" : [['b', 'B'], ['ε']]
}

letter_sentence= [['a', 'a', 'b', 'b', 'a', 'a', ' ']]
letter_list = [['S', ['A', 'B']], ['A', ['a', 'A']], ['A', ['a', 'A']], ['A', ['ε']],
                ['B', ['b', 'B']], ['B', ['b', 'B']], ['B', ['ε']]]

#################################################################################################

word_dict = {
    "<sentence>" : [['<noun-phrase>', '<verb-phrase>']],
    "<noun-phrase>" : [['<determiner>', '<noun>']],
    "<verb-phrase>" : [['<verb>'], ['<verb>', '<noun-phrase>']],
    "<determiner>" : [['the'], ['a']],
    "<noun>" : [['cat'], ['dog'], ['man'], ['telescope']],
    "<verb>" : [['saw'], ['liked'], ['admired']]
}

word_sentence = [['a', 'man', 'killed', 'the', 'dog']]
word_list = [['<sentence>', ['<noun-phrase>', '<verb-phrase>']], ['<noun-phrase>', ['<determiner>', '<noun>']],
              ['<determiner>', 'a'], ['<noun>', 'man'], ['<verb-phrase>', ['<verb>', '<noun-phrase>']],
                ['<noun-phrase>', ['<determiner>', '<noun>']]]

#################################################################################################

keys = set(word_dict.keys())

def find_correct_part(data, keys):
    correct_part_list = []
    for item in data:
        right = item[1]
        values = right if isinstance(right, list) else [right]
        for v in values:
            if v not in keys:
                correct_part_list.append(v)
    return correct_part_list

#print(find_correct_part(word_list, keys))
print(find_correct_part(letter_list, set(letter_dict.keys())))



def find_where_occurs(correct_part_list, sentence,is_word_based=True):
    if is_word_based:
        error_token = sentence[0][len(correct_part_list)]
        print(f"Where the error occurs: at token {len(correct_part_list)+1} (\"{error_token}\") ")
    else:
        epsilon_counter = correct_part_list.count('ε')
        error_token = sentence[0][len(correct_part_list)-epsilon_counter]
        print(f"Where the error occurs: at token {len(correct_part_list)+1 - epsilon_counter} (\"{error_token}\") ")

#find_where_occurs(find_correct_part(word_list, set(word_dict.keys())), word_sentence, is_word_based=True)
find_where_occurs(find_correct_part(letter_list, set(letter_dict.keys())), letter_sentence, is_word_based=False)

def find_expected_values(list_for_json, grammar_dict):
    expected_values = []
    correct_part_list = find_correct_part(list_for_json, set(grammar_dict.keys()))
    last_correct_token = correct_part_list[-1]
    
    if len(correct_part_list) > 0:
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
            return "No expected values found.Current key is unknown."
    
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
            return f"What was expected: a {expected_key.strip('<>')} ({result}) " + end_of_error_message
        else:
            return f"What was expected: a {expected_key.strip('<>')} (\"{expected_values[0]}\") " + end_of_error_message
    


#print(find_expected_values(word_list, word_dict)) 
print(find_expected_values(letter_list, letter_dict)) # word_list & letter_listaslında list_for_json listesidir...

