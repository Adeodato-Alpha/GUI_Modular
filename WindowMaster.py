from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class RootGUI():
    def __init__(self,serial,data):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("Serial communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")
        self.data = data
        self.serial = serial

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        print("Closing the window and exit")
        self.root.destroy()
        self.serial.SerialClose(self)
        self.serial.threading = False


# Class to setup and create the communication manager with MCU
class ComGui():
    def __init__(self, root, serial,data):
        '''
        Initialize the connexion GUI and initialize the main widgets 
        '''
        # Initializing the Widgets
        self.root = root
        self.serial = serial
        self.data =data
        
        self.frame = LabelFrame(root, text="Com Manager",
                                padx=5, pady=5, bg="white")
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w")
        
        # Setup the Drop option menu
        self.ComOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_refresh = Button(self.frame, text="Refresh",
                                  width=10,  command=self.com_refresh)
        self.btn_connect = Button(self.frame, text="Connect",
                                  width=10, state="disabled",  command=self.serial_connect)

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

        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)

    def ComOptionMenu(self):
        '''
         Method to Get the available COMs connected to the PC
         and list them into the drop menu
        '''
        # Generate the list of available coms

        self.serial.getCOMList()

        self.clicked_com = StringVar()
        self.clicked_com.set(self.serial.com_list[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *self.serial.com_list, command=self.connect_ctrl)

        self.drop_com.config(width=10)

   
    def connect_ctrl(self, widget):
        '''
        Mehtod to keep the connect button disabled if all the 
        conditions are not cleared
        '''
        print("Connect ctrl")
        # Checking the logic consistency to keep the connection btn
        if "-" in self.clicked_com.get():
            self.btn_connect["state"] = "disabled"
        else:
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        print("Refresh")
        # Get the Widget destroyed
        self.drop_com.destroy()

        # Refresh the list of available Coms
        self.ComOptionMenu()

        # Publish the this new droplet
        self.drop_com.grid(column=2, row=2, padx=self.padx)

        # Just in case to secure the connect logic
        logic = []
        self.connect_ctrl(logic)

    def serial_connect(self):
        if self.btn_connect["text"] in "Connect":
            # Start the serial communication
            self.serial.SerialOpen(self)

            # If connection established move on
            if self.serial.ser.status:
                # Update the COM manager
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_com["state"] = "disable"
                InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"
                messagebox.showinfo("showinfo", InfoMsg)

                # Display the channel manager
                self.conn = ConnGUI(self.root, self.serial,self.data)
                self.serial.t1 = threading.Thread(
                    target=self.serial.SerialSync, args=(self,),daemon=True
                )
                self.serial.t1.start()
            else:
                ErrorMsg = f"Failure to estabish UART connection using {self.clicked_com.get()} "
                messagebox.showerror("showerror", ErrorMsg)
        else:
            self.serial.threading = False
            self.conn.graph = False
            # Closing the Serial COM
            # Close the serial communication
            self.serial.SerialClose(self)

            # Closing the Conn Manager
            # Destroy the channel manager
            self.conn.ConnGUIClose()
            self.data.ClearData()
            InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_com["state"] = "active"


class ConnGUI():
    def __init__(self, root, serial,data):
        '''
        Initialize main Widgets for communication GUI
        '''
        self.data = data
        self.root = root
        self.serial = serial
        self.graph = False
        # Build ConnGui Static Elements
        self.frame = LabelFrame(root, text="Connection Manager",
                                padx=5, pady=5, bg="white", width=60)
        self.sync_label = Label(
            self.frame, text="Sync Status: ", bg="white", width=15, anchor="w")
        self.sync_status = Label(
            self.frame, text="..Sync..", bg="white", fg="orange", width=5)

        self.ch_label = Label(
            self.frame, text="Active channels: ", bg="white", width=15, anchor="w")
        self.ch_status = Label(
            self.frame, text="...", bg="white", fg="orange", width=5)

        self.btn_start_stream = Button(self.frame, text="Start", state="disabled",
                                       width=5, command=self.start_stream)
        
        self.btn_start_gph = Button(self.frame, text="Start", state="disabled",
                                       width=5, command=self.UpdateChart)
        self.btn_stop_stream = Button(self.frame, text="Stop", state="disabled",
                                      width=5, command=self.stop_stream)

        self.btn_add_chart = Button(self.frame, text="+", state="disabled",
                                    width=5, bg="white", fg="#098577",
                                    command=self.new_chart)

        
        self.save = False
        self.SaveVar = IntVar()
        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar,
                                      onvalue=1, offvalue=0, bg="white", state="disabled",
                                      command=self.save_data)

        self.separator = ttk.Separator(self.frame, orient='vertical')

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 15

        # Extending the GUI
        self.ConnGUIOpen()
        self.chartMaster = DisGUI(self.root, self.serial,self.data)

    def ConnGUIOpen(self):
        '''
        Method to display all the widgets 
        '''
        self.root.geometry("800x120")
        self.frame.grid(row=0, column=4, rowspan=3,
                        columnspan=5, padx=5, pady=5)

        self.sync_label.grid(column=1, row=1)
        self.sync_status.grid(column=2, row=1)

        self.ch_label.grid(column=1, row=2)
        self.ch_status.grid(column=2, row=2, pady=self.pady)

        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)
        
        self.btn_start_gph.grid(column=5, row=1, padx=self.padx)
        self.btn_add_chart.grid(column=4, row=1, padx=self.padx)

        self.save_check.grid(column=4, row=2, columnspan=2)
        self.separator.place(relx=0.58, rely=0, relwidth=0.001, relheight=1)

    def ConnGUIClose(self):
        '''
        Method to close the connection GUI and destorys the widgets
        '''
        # Must destroy all the element so they are not kept in Memory
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("360x120")

    def start_stream(self):
        self.btn_start_stream["state"]="disabled"
        self.btn_stop_stream["state"]="active"
        self.serial.t1 = threading.Thread(target=self.serial.SerialDataStream,args=(self,),daemon=True)
        self.serial.t1.start()
        
    def startgraph(self):
        if self.graph:
                self.graph = False
        else:
                self.graph = True
    def UpdateChart(self):
        try:
            
                self.chartMaster.ax.clear()
                self.char = self.chartMaster.ax
                self.y = self.data.Ydis[0]
                self.x = self.data.Xdis
                self.data.plotingShit(self)
                self.chartMaster.fig.canvas.draw()
        except Exception as e:
            print(e)
    def stop_stream(self):
        self.btn_start_stream["state"]="active"
        self.btn_stop_stream["state"]="disabled"
        self.serial.threading = False

    def new_chart(self):
        self.chartMaster.AddChannelMaster()

    def kill_chart(self):
        pass

    def save_data(self):
        pass

class DisGUI():
    def __init__(self,root,serial,data):
        self.root = root
        self.serial = serial
        self.data = data

        self.frameCol = 0
        self.frameRow=4
    def AddChannelMaster(self):
        self.AddMasterFrame()
        self.AdjustRootFrame()
        self.AddGraph()
    def AddMasterFrame(self):
        self.frame = LabelFrame(self.root, text="Displayed Manager", padx=5,pady=5, bg="white")
        self.frame.grid(padx=5,column=self.frameCol,row=self.frameRow,columnspan=9,sticky=NW)
    def AdjustRootFrame(self):
        RootWD = 800
        RootH = 600
        self.root.geometry(f"{RootWD}x{RootH}")
    def AddGraph(self):
        self.fig = plt.Figure(figsize=(7,5),dpi=80)
        self.ax= self.fig.add_subplot(111)
        self.graphic = FigureCanvasTkAgg(self.fig, master = self.frame)
        self.graphic.get_tk_widget().grid(column=1,row=0,columnspan=4,sticky=N)

if __name__ == "__main__":
    RootGUI()
    ComGui()
    ConnGUI()
    #DisGUI()