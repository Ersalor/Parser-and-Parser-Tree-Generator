import functions
#Kullanıcıdan grammer dosyası alınır
grammar_file = input("Enter the grammar file name: ").strip()

#Dosya açılır ve okunur
grammer_dict=functions.grammar_to_dict(grammar_file)

#Kelime bazlı mı yoksa karakter bazlı mı olduğunu kontrol edilir
#print(functions.is_word_based(grammer_dict))


#Stringler tokenize edilir
"""sentence_file = input("Enter the sentence file name: ").strip()

with open(sentence_file, 'r', encoding='utf-8') as file:
    sentence_row = []
    for line in file:
        line = line.strip()
        if line:
            sentence_row.append(line)

for sentence in sentence_row:
    print(f"Sentence: {sentence}")"""
