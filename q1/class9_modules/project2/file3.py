with open ("text_file3.txt" , "w") as file1:
    file1.write("Hello World")
    file1.seek(20)
    file1.write("Hello World10")
    