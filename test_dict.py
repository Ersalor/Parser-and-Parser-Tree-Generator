
import json


tree={}

dict= {"  <sentence>" : [['<noun-phrase>', '<verb-phrase>']],
    "<noun-phrase>" : [['<determiner>', '<noun>']],
    "<verb-phrase>" : [['<verb>'], ['<verb>', '<noun-phrase>']],
    "<determiner>" : [['the'], ['a']],
    "<noun>" : [['cat'], ['dog'], ['man'], ['telescope']],
    "<verb>" : [['saw'], ['liked'], ['admired']]
    }

print(json.dumps(dict, indent=2))





