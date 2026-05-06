import json

#######################################################################################
#                        Parse Tree Printing Function
#######################################################################################

def print_parse_tree(tree_dict, indent=""):
    # Sözlükteki elemanları (dalları) sırayla geziyoruz
    items = list(tree_dict.items())
    
    for i, (key, value) in enumerate(items):
        is_last = (i == len(items) - 1)
        # Son elemansa "└──", değilse "├──" kullanıyoruz
        prefix = "└── " if is_last else "├── "
        
        # Düğümün kendisini (Non-Terminal veya Terminal kuralı) yazdır
        print(indent + prefix + str(key))
        
        # Eğer bu düğümün altında başka dallar (sözlük) varsa, içeri doğru özyinelemeli dal
        if isinstance(value, dict):
            # Alt dallar için girintiyi (indentation) ayarla
            extension = "    " if is_last else "│   "
            print_parse_tree(value, indent + extension)
            
        # Eğer bu düğümün değeri düz bir metinse (Uçbirim/Terminal ise), onu da yaprak olarak yazdır
        elif isinstance(value, str):
            extension = "    " if is_last else "│   "
            # Kelimeyi [ "kelime" ] formatında belirginleştir
            print(indent + extension + "└── [ \"" + value + "\" ]")

#######################################################################################
#                                  Word Based
#######################################################################################

def generate_json_from_list_word(flat_parse_list):
    # Listeyi bir yineleyiciye (iterator) çeviriyoruz. 
    # Böylece next() ile elemanları sırayla tek tek yutacağız.
    iterator = iter(flat_parse_list)

    def build_tree():
        try:
            # Sıradaki düğümü al (Örn: ['<noun>', 'man'])
            node = next(iterator)
        except StopIteration:
            return None, None

        # Proje gereksinimi: '<' ve '>' işaretlerini temizle
        raw_key = node[0]
        key = raw_key.replace("<", "").replace(">", "")
        value = node[1]

        # 1. Terminal Durumu: Eğer value bir string ise (Örn: 'man'), en alt daldıyız.
        if isinstance(value, str):
            return key, value

        # 2. Non-Terminal Durumu: Eğer value bir listeyse (Örn: ['<determiner>', '<noun>']), alt dallar vardır.
        children_dict = {}
        
        # 'value' listesinde kaç tane alt eleman varsa, ağaçtan o kadar parça koparmamız gerekiyor.
        for _ in range(len(value)):
            child_key, child_val = build_tree()
            if child_key:
                children_dict[child_key] = child_val

        return key, children_dict

    # Özyinelemeli inşa sürecini başlat
    root_key, root_tree = build_tree()

    # En dıştaki ana Sözlüğü (Dictionary) oluştur
    final_dict = {root_key: root_tree}
    
    # Python Sözlüğünü, girintili (indent=4) ve okunabilir bir JSON stringine çevir
    return json.dumps(final_dict, indent=4, ensure_ascii=False)

list_for_json_word = [['<sentence>', ['<noun-phrase>', '<verb-phrase>']], ['<noun-phrase>', ['<determiner>', '<noun>']], ['<determiner>', 'a'], ['<noun>', 'man'], ['<verb-phrase>', ['<verb>', '<noun-phrase>']], ['<verb>', 'admired'], ['<noun-phrase>', ['<determiner>', '<noun>']], ['<determiner>', 'the'], ['<noun>', 'dog']]

json_format_word= generate_json_from_list_word(list_for_json_word)
print(json_format_word)

json_to_dict_word = json.loads(json_format_word)

print("Parse Tree:")
print_parse_tree(json_to_dict_word)

#######################################################################################
#                                  Letter Based
#######################################################################################
def generate_json_from_list_letter(flat_parse_list):
    if not flat_parse_list:
        return "{}"

    # 1. Non-Terminal (Kural) Tespiti:
    # Listenin sol tarafındaki her şey kuraldır ('S', 'A', 'B'). 
    # Bunları bir kümeye alıyoruz ki terminal/non-terminal ayrımını sistem kendi anlasın.
    non_terminals = set([item[0] for item in flat_parse_list])
    
    # 2. Listeyi yineleyiciye (stream) çeviriyoruz.
    iterator = iter(flat_parse_list)

    def build_tree(symbol):
        # Eğer gelen sembol bir kural değilse (yani 'a', 'b' veya 'ε' gibi bir terminalse)
        # Listeden hiçbir şey ÇEKME! Doğrudan sembolün kendisini yaprak (leaf) olarak dön.
        if symbol not in non_terminals:
            return symbol
        
        # Eğer sembol bir kural ise, listeden sıradaki açılımı çek (Tüketim)
        try:
            node = next(iterator)
        except StopIteration:
            return None
        
        rhs = node[1] # Sağ taraf (Örn: ['a', 'A'] veya sadece 'b')
        
        # Eğer sağ taraf sadece düz bir string ise (Listenin sonundaki ['B', 'b'] durumu)
        # Üzerinde döngü kurabilmek için onu listeye çeviriyoruz.
        if isinstance(rhs, str):
            rhs = [rhs]

        children_dict = {}
        # Kuralın sağ tarafındaki her bir parça için özyinelemeli (recursive) olarak dallan
        for child in rhs:
            child_val = build_tree(child)
            # Json anahtarlarını oluştur (Gramer 1 için < > temizliği, Gramer 2'yi bozmaz)
            clean_child = child.replace("<", "").replace(">", "")
            children_dict[clean_child] = child_val
        
        return children_dict

    # Motoru ilk kural ile (Listenin en başındaki S) ateşle
    root_symbol = flat_parse_list[0][0]
    root_tree = build_tree(root_symbol)

    # En dıştaki sözlüğü (JSON objesini) oluştur
    final_dict = {root_symbol.replace("<", "").replace(">", ""): root_tree}
    
    # İnsan tarafından okunabilir formata dönüştür
    return json.dumps(final_dict, indent=4, ensure_ascii=False)

list_for_json_letter= [['S', ['A', 'B']], ['A', ['a', 'A']], ['A', ['a', 'A']], ['A', ['a', 'A']], ['A', ['ε']], ['B', ['b', 'B']], ['B', ['b', 'B']], ['B', 'b']]

json_format_letter= generate_json_from_list_letter(list_for_json_letter)
print(json_format_letter)

json_to_dict_letter= json.loads(json_format_letter)

print("Parse Tree:")
print_parse_tree(json_to_dict_letter)
