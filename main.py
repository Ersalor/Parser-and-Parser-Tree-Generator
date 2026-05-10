import functions

#Kullanıcıdan grammar ve sentences dosyaları alınır
grammar_file = "grammar2.txt"#input("Enter the grammar file name: ").strip()
sentence_file = "sentences2.txt"#input("Enter the sentence file name: ").strip()

#Grammar ve sentences dosyaları işlenir, doğruluk kontrolü yapılır, JSON formatına dönüştürülür ve parse tree görselleştirilir
functions.execute_parsing_and_visualization(grammar_file, sentence_file)

