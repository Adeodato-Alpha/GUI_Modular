import serial.tools.list_ports  
import time
import threading


class SerialCtrl():
    def __init__(self):
        '''
        Initializing the main varialbles for the serial data
        '''
        self.sync_cnt = 500
        pass

    def getCOMList(self):
        '''
        Method that get the lost of available coms in the system
        '''
        ports = serial.tools.list_ports.comports()
        self.com_list = [com[0] for com in ports]
        self.com_list.insert(0, "-")

    def SerialOpen(self, ComGUI):
        '''
        Method to setup the serial connection and make sure to go for the next only 
        if the connection is done properly
        '''

        try:
            self.ser.is_open
        except:
            PORT = ComGUI.clicked_com.get()
            self.ser = serial.Serial()
            self.ser.port = PORT
            self.ser.timeout = 0.1

        try:
            if self.ser.is_open:
                print("Already Open")
                self.ser.status = True
            else:
                PORT = ComGUI.clicked_com.get()
                self.ser = serial.Serial()
                self.ser.port = PORT
                self.ser.timeout = 0.01
                self.ser.open()
                self.ser.status = True
        except:
            self.ser.status = False

    def SerialClose(self, ComGUI):
        '''
        Method used to close the UART communication
        '''
        try:
            self.ser.is_open
            self.ser.close()
            self.ser.status = False
        except:
            self.ser.status = False
    def SerialSync(self, gui):
        self.threading = True
        cnt = 0
        while self.threading:
            try:
                #self.ser.write(gui.data.sync.encode())
                gui.conn.sync_status["text"] = "..Sync.."
                gui.conn.sync_status["fg"] = "orange"
                gui.data.RowMsg = self.ser.readline()
                # print(f"RowMsg: {gui.data.RowMsg}")
                gui.data.DecodeMsg()
                
                if gui.data.channels> 0:
                    
                    gui.conn.btn_start_stream["state"] = "active"
                    gui.conn.btn_add_chart["state"] = "active"
                    gui.conn.btn_start_gph["state"] = "active"
                    gui.conn.save_check["state"] = "active"
                    gui.conn.sync_status["text"] = "OK"
                    gui.conn.sync_status["fg"] = "green"
                    gui.conn.ch_status["text"] = gui.data.channels
                    gui.conn.ch_status["fg"] = "green"
                    gui.data.SynchChannel = gui.data.channels
                    gui.data.buildYdata()
                    print(gui.data.YData)
                    self.threading == False 
                    break
                   
                    
                if self.threading == False:
                    break
            except Exception as e:
                print(e)
            cnt += 1
            if self.threading == False:
                break
            if cnt > self.sync_cnt:
                self.threading = False
                    
                cnt = 0
                gui.conn.sync_status["text"] = "failed"
                gui.conn.sync_status["fg"] = "red"
                time.sleep(0.5)
                if self.threading == False:
                    break
    def SerialDataStream(self,gui):
        self.threading = True
        cnt = 0
        while self.threading:
            try:
                gui.data.RowMsg = self.ser.readline()
                # print(f"RowMsg: {gui.data.RowMsg}")
                gui.data.DecodeMsg()
                if gui.data.SynchChannel ==8:
                    gui.data.SetRefTime()
                    break
            except Exception as e:
                print(e)
        while self.threading:
            try:
                gui.data.RowMsg = self.ser.readline()
                # print(f"RowMsg: {gui.data.RowMsg}")
                gui.data.DecodeMsg()
                if gui.data.SynchChannel ==8:
                    gui.data.UpdataXdata()
                    gui.data.UpdataYdata()
                    gui.data.AdjustData()
                
                    #print(gui.data.Ydis)
                #Ysam = [Ys[len(gui.data.XData)-1] for Ys in gui.data.YData]
                #print(f"x: {gui.data.XData[len(gui.data.XData)-1]}  y:{Ysam}")
                #print(f"{len(gui.data.XData)}, {len(gui.data.YData[0])}")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    SerialCtrl()