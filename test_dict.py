import json

def generate_json_from_list(flat_parse_list):
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

# ---- KULLANIMI ----
liste= [['<sentence>', ['<noun-phrase>', '<verb-phrase>']], ['<noun-phrase>', ['<determiner>', '<noun>']], ['<determiner>', 'a'], ['<noun>', 'man'], ['<verb-phrase>', ['<verb>', '<noun-phrase>']], ['<verb>', 'admired'], ['<noun-phrase>', ['<determiner>', '<noun>']], ['<determiner>', 'the'], ['<noun>', 'dog']]

json_ciktisi = generate_json_from_list(liste)
print(json_ciktisi)