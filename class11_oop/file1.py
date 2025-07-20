import random

class House:
    def __init__(self,addrs):
        #self.address = "ABC",random.randint(1,100)
        self.address = addrs
        self.number_of_rooms = 4
        self.number_of_doors = 2
    
    def ring_bell(self):
        print("Ding Dong")


h1 = House("A123")
print (h1.address)
h1.ring_bell()