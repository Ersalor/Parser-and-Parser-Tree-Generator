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