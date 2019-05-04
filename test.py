filename = "./../datasets/Birt.txt"


ss = []
with open(filename) as fo:
    i = 0
    for line in fo:
        i += 1
        if(i >= 3):
            break;
        ss = line.split("\t") 

for s in ss:
    print(s)
