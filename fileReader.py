# f = open('results.txt', 'r')
# line = f.readline()

# array = line.split('(')

# for arr in array:
#     print(arr.replace("', '", "\n"))
test = ['linkA', 'linkB']
f = open("demofile2.txt", "w")
f.write("Now the file has more content!")
f.write("And even more content")
f.writelines(test)
f.close()

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())