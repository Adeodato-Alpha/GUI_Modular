import time
import numpy as np
class DataMaster():
    def __init__(self):
        
        self.SynchChannel = 0
        self.channels = 0
        self.msg = 0
        self.XData = []
        self.YData = []
        self.DisplayTimeRange = 5

    def DecodeMsg(self):
        temp = self.RowMsg.decode('ascii').strip().split(',')
        temp= [s for s in temp if s.strip()]
        if len(temp)>0:
            
            self.channels = len(temp)
            self.msg = temp
        
        '''
        if len(temp) > 0:
            if "#" in temp:
                self.msg = temp.split("#")
                # print(f"Before removing index :{self.msg}")
                del self.msg[0]
                # print(f"After removing index :{self.msg}")
        '''

    def GenChannels(self):
        self.Channels = [f"Ch{ch}" for ch in range(self.SynchChannel)]

    def buildYdata(self):
        for _ in range(self.SynchChannel):
            self.YData.append([])

    def ClearData(self):
        self.RowMsg = ""
        self.msg = 0
        self.Ydata = []
    def SetRefTime(self):
        if len(self.XData) == 0:
            self.RefTime = time.perf_counter()
        else:
            self.RefTime = time.perf_counter() - self.XData[len(self.XData)-1]

    def UpdataXdata(self):
        if len(self.XData) == 0:
            self.XData.append(0)
        else:
            self.XData.append(time.perf_counter()-self.RefTime)

    def UpdataYdata(self):
        for ChNumber in range(self.SynchChannel):
            self.YData[ChNumber].append(self.msg[ChNumber])
    def AdjustData(self):
        lenXdata = len(self.XData)
        if (self.XData[lenXdata-1]-self.XData[0])> self.DisplayTimeRange:
            del self.XData[0]
            for ydata in self.YData:
                del ydata[0]
        x = np.array(self.XData)
        self.Xdis = np.linspace(x.min(), x.max(), len(x), endpoint=0)
        self.Ydis=  np.array(self.YData)

    def plotingShit(self,gui):
        gui.char.plot(gui.x,gui.y)
