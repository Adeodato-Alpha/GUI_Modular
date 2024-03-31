from tkinter import *
#inicializar Root de la Ventana
#Rolandos new Branch 
class RootWindow:
    def __init__(self,title,size) :
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.root.config(bg="white")

class ConectFrame():
    def __init__(self,root) :
        self.root = root
        self.frame = LabelFrame(root, text="Conección a uC",padx=5, pady=5, bg="white")
        self.label_com = Label(self.frame, text="Puerto(s) Disponibles: ", bg="white", width=15, anchor="w")
        self.ComOptionMenu()
        self.ButtonConect = Button(self.frame, text= "Conectar",state="disabled")
        self.ButtonRefresh = Button(self.frame,text="Recargar Puertos")
        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()       
    def publish(self):
        '''
         Method to display all the Widget of the main frame
        '''
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        self.label_com.grid(column=1, row=2)
        self.drop_com.grid(column=2, row=2, padx=self.padx)
        self.ButtonConect.grid(column=3, row=3, padx=self.padx)
        self.ButtonRefresh.grid(column=3,row=2,padx= self.padx)
    def ComOptionMenu(self):
        '''
         Method to Get the available COMs connected to the PC
         and list them into the drop menu
        '''
        # Generate the list of available coms

        coms = ["-", "COM3"]

        self.clicked_com = StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *coms)

        self.drop_com.config(width=10)

if __name__ == "__main__":
    RootWindow()
    ConectFrame()