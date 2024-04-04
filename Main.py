from WindowMaster import *
from COMsClass import *
_RootMain = RootGUI()
_SerialInit = SerialCtrl()
Comunication = ComGui(_RootMain.root,_SerialInit)
_RootMain.root.mainloop()