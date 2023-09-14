from tkinter import *

root = Tk()
root.title("Depth")



#Maximal Value bekommen
def getdepth():
    tick =var.get()
    if tick != "MAXPAGES":
        tick = mystring.get()
    print(tick)

#Freie Wahl der Pages
mystring = StringVar()
Label(root, text="Enter the pages you want to screen").pack()
Entry(root, textvariable=mystring).pack()

var = StringVar()#hier definiere ich was rauskommt
c = Checkbutton(root, text="USE MAX DEPTH", variable=var, onvalue="MAXPAGES")
c.pack()

get_depth_button = Button(root, text="SUBMIT", command=getdepth).pack()

root.mainloop()