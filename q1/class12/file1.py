#class and objects are 2 main things in oop
#class is the blue print
#constructor function class k object banane mai help krega
#class mai properties/attributes and methods hote hain

#properties
##address/no of rooms/ no of doors/ etc

#methods
##ring bell/call/lift

class house:
    def __init__(self,addr):
        #{} self add krne se ek blank object create hojayega uski value empty hogi, phr usmai ek ek kr k cheeze add hojati hain
        #self.address : str = "123"
        self.address : str = addr
        self.no_of_doors : int = 2
        self.no_of_rooms : int = 4
    
    def call_lift(self):
        print(f"{self.address} lift is called")

h1 = house("A-123")    # {address, no_of_doors, no_of_rooms} ye self ka object pura h1 mai store hojayega 
h2 = house("B-123")
h3 = house("C-123")


print(h1.address)
print(h2.address)
print(h3.address)

h1.call_lift()

