#file_name = input("Enter the file name: ")
file = open("grammar1.txt", "r")

file_row = []
dict = {}

for line in file:
    print(line.strip())
    file_row.append(line.strip())

print()

for line in file_row:
    if "|" in line :
        dict[line.split("::=")[0].strip()] = line.split("::=")[1].strip().split("|")

    else:
        dict[line.split("::=")[0].strip()] = line.split("::=")[1].strip()


for key in dict:
    print(key, ":", dict[key])

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
                        gotovalue(grammer_dict,j)
                if i in grammer_dict:   
                    gotovalue(grammer_dict,i)
                else:
                     print(grammer_dict[i]) #burda biryerde değişiklik yapıcam
                     break                  #en son terminalleden birini seçip iç içe döngüyü bırakması lazım onu sağlayacağım
        else:
           pass

