file = open("text_file.txt" , "w")
file.write("Hello World")
file.close()

with open ("text_file2.txt" , "a") as file1:
    file1.write("\nHello World5")
