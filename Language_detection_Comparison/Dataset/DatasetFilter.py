f = open("x_train.txt", "r")
x = f.readlines()
f.close()
f = open("y_train.txt", "r")
y = f.readlines()
f.close()

x_new = open("x_new_train.txt", "w")
y_new = open("y_new_train.txt", "w")
lang = ["eng", "fra", "slk", "slv", "ita", "deu", "spa", "nld"]
length = len(y)

for language in lang:
    for i in range(length):
        if(y[i].rstrip()==language):
            x_new.write(x[i])
            y_new.write(y[i])
x_new.close()
y_new.close()

