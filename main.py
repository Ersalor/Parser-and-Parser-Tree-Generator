#Kullanıcaıdan grammer dosyası alınır
file_name = input("Enter the grammar file name: ").strip()

#Dosya açılır ve okunur
with open(file_name, 'r', encoding='utf-8') as file:
    lines=file.readlines()

#Grammer dosyasından dictionary oluşturulur
grammar = {}
for line in lines:
    line = line.strip()
    if not line:
        continue   
    left, right = line.split('::=')
    left = left.strip()
    right = right.strip()
    right_parts = [part.strip() for part in right.split('|')]
    for part in right_parts:
        right_parts[right_parts.index(part)] = part.split(" ")
    grammar[left] = right_parts

#Grammer dosyasından üretilen dictionary yazdırılır
print("Grammar Dictionary: \n")
for key, value in grammar.items():
    print(f"{key} ::= {value}")

#Her bir seçeneğin birer liste olarak dictionary'e eklenmesi gerekiyordu.
#Detaylarını anlatıcam...
