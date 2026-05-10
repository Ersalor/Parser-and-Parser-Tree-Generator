letter_dict = {
    "S": [['A', 'B']],
    "A": [['a', 'A'], ['ε']],
    "B": [['b', 'B'], ['ε']]
}

letter_dict2 = {
    "S": [['A', 'B']],
    "A": [['a', 'A'], ['a']],
    "B": [['b', 'B'], ['b', 'b']]
}

def find_expected_values_letter(list_for_json, grammar_dict):

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
            return f"What was expected: a {key} ({result}) {end_msg}"
        elif len(values) == 1:
            return f"What was expected: a {key} (\"{values[0]}\") {end_msg}"
        else:
            return "No expected values found."

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


# ─── TESTLER ────────────────────────────────────────────────────────────────

# Test 1: Epsilon grammar, yanlış cümle → B ("b") to continue
list1 = [['S', ['A', 'B']], ['A', ['a', 'A']], ['A', ['a', 'A']], ['A', ['ε']],
          ['B', ['b', 'B']], ['B', ['b', 'B']], ['B', ['ε']]]
print("Test 1:", find_expected_values_letter(list1, letter_dict))

# Test 2: Epsilon yok, yanlış cümle → B ("b") to continue
list2 = [['S', ['A', 'B']], ['A', ['a', 'A']], ['A', 'a'], ['B', ['b', 'B']]]
print("Test 2:", find_expected_values_letter(list2, letter_dict2))

# Test 3: Liste boş → to start
print("Test 3:", find_expected_values_letter([], letter_dict))

# Test 4: Epsilon grammar, hata çok erken (sadece S var) → A ("a") to continue
list4 = [['S', ['A', 'B']]]
print("Test 4:", find_expected_values_letter(list4, letter_dict))

# Test 5: Epsilon yok, hata çok erken (sadece S var) → A ("a") to continue
list5 = [['S', ['A', 'B']]]
print("Test 5:", find_expected_values_letter(list5, letter_dict2))