items = ["hara dhaniya" , "podina" , "Dahi" , "Andey"]

# print(type(items))

# print(items)
# print(items[1])
# print(len(items))
count = 0

for x in items:
    #print (f"{count} , {items[count]}")
    count = count+1

#items.pop(1)
items.append("Roti")
items.insert(3, "Allu")
items.pop(0)
items.remove("Dahi")


print(items)

