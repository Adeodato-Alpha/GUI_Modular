from tkinter import *
#Handrea branch

#inicializar Root de la Ventana
class RootWindow:
    def __init__(self,title,size) :
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.root.config(bg="white")

class ConectFrame():
    def __init__(self,root) :
        self.root = root
        self.frame = LabelFrame(root, text="Com Manager",padx=5, pady=5, bg="white")
        self.label_com = Label(self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w")
        self.label_bd = Label(self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w")
        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()       

if __name__ == "__main__":
    RootWindow()
    ConectFrame()