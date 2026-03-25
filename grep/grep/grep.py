file_name = input("enter filename:")
pattern = input("enter pattern:")

file = open (file_name, "r")

line = file.readline()

while line:
    if pattern in line:
        print(line)
    line = file.readline()
