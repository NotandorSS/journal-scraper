f = open('results.txt', 'r')
line = f.readline()

array = line.split('(')

for arr in array:
    print(arr.replace("', '", "\n"))