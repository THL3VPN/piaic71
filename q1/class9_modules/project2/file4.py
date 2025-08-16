#write and read
# with open ("text_file4.txt" , "w+") as file1:     
#     file1.write("Hello World4")
#     file1.seek(0)
#     print(file1.read())

#read and append
with open ("text_file4.txt" , "r+") as file1:       
    print(file1.read())
    file1.write("Hello World4\n")


