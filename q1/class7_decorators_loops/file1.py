#kisi function k parameter mai koi doosra function call kren aur 
#usko usi function mai call krlen to use call backfunction kehte hain

def function1(callingFunction2):    
    print("calling function 1")
    callingFunction2()

def function2():
    print("calling function 2")

function1(function2)    #Reference dene k lye "()" lagane ki zaroort nai argument mai

#dacorators apke function k around ek wraper bana deta hai


