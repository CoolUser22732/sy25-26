filename = "BeeMovieScript.txt"
file = open(filename, "r")

line = file.readline()
while line:
    print(line)
    line = file.readline()

file.close()