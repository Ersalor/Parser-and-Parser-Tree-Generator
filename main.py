#file_name = input("Enter the file name: ")
file = open("grammar1.txt", "r",encoding="utf-8")

file_row = []
dict = {}

for line in file:
    #print(line.strip())
    file_row.append(line.strip())

print()

for line in file_row:
        dict[line.split("::=")[0].strip()] = line.split("::=")[1].strip().split(" | ")

print(dict)

#print(list(dict.keys())[0])

def gotovalue(grammer_dict,key):
      
      if key in grammer_dict:
            value = grammer_dict[key]
            if type(value) != list:
                value_list = value.split(" ")
            elif type(value) == list:
                value_list = value
            for i in value_list:
                if len(i.split(" ")) > 1:
                    for j in i.split(" "):
                         if j in grammer_dict:
                              gotovalue(grammer_dict,j)
                    if i in grammer_dict:   
                        gotovalue(grammer_dict,i)