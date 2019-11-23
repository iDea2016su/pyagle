#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import threading
import queue
import time
import re
import serial

class WarnValue:
    upValue = 0
    downValue = 0
    averageValue = 0
    def __init__(self,avr):
        self.upValue = 0
        self.downValue = 0
        self.averageValue = avr

    def AddUp10(self):
        self.upValue = self.upValue + 10
        return

    def AddUp1(self):
        self.upValue = self.upValue + 1
        return

    def SubUp10(self):
        self.upValue = self.upValue - 10
        return

    def SubUp1(self):
        self.upValue = self.upValue -1
        return

    def AddDown10(self):
        self.downValue = self.downValue + 10
        return

    def AddDown1(self):
        self.downValue = self.downValue +1
        return

    def SubDown10(self):
        self.downValue = self.downValue - 10
        return

    def SubDown1(self):
        self.downValue = self.downValue -1
        return

    def getUpValue(self):
        return self.upValue

    def getDownValue(self):
        return self.downValue

class Filter:
    Q = 0.01
    R = 1.0
    A = 1.0
    C = 1.0
    X_pre = 1.0
    P_pre = 1.0
    Xkf_k1 = 0.0  #chushizhi
    P_k1 = 1.0
    Kg = 0.0
    currentValue = 0

    def filter(self,val):
        self.X_pre = self.A * self.Xkf_k1
        self.P_pre = self.P_k1 + self.Q
        self.Kg = self.P_pre / (self.P_pre + self.R)
        self.Xkf_k1 = self.X_pre + self.Kg * (val- self.C * self.X_pre)
        self.P_k1 = (1 - self.Kg * self.C) * self.P_pre
        self.currentValue = self.Xkf_k1

    def get(self):
        return self.currentValue

class List:
    array = [143,143,143,143,143,143,143,143,\
             143,143,143,143,143,143,143,143,\
             143,143,143,143,143,143,143,143,\
             143,143,143,143,143,143,143,143,\
             143,143,143,143,143,143,143,143,\
             143,143,143,143,143,143,143,143]
    def __init__(self):
        pass
    def add(self,val):
        j = 0
        while(j<47):
            self.array[j] = self.array[j+1]
            j = j + 1
        self.array[47] = val
        return

    def get(self):
        #print(str(self.array))
        return self.array

class Seriar:
    def __init__(self, Port='COM6'):
        # 构造串口的属性
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = Port
        self.ID = None
        self.data = None
     #定义串口等待的函数

    def setPort(self,port):
        self.port = port

    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
            self.alive = False
            self.stop()
    #启动串口的函数
    def start(self):
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = 9600
        #设置等待时间，若超出这停止等待
        self.l_serial.timeout = 2
        self.l_serial.open()
        #判断串口是否已经打开
        if self.l_serial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True
            self.thread_read = None
           # self.thread_read = threading.Thread(target=self.FirstReader)
            self.thread_read.setDaemon(1)
            self.thread_read.start()
            return True
        else:
            return False

#复选框状态
upCheckStatus = 0
downCheckStatus = 1
checkCount = 0
def CheckCallBack():
    global checkCount
    global upCheckStatus
    global downCheckStatus
    checkCount = checkCount +1
    if(checkCount%2):
        upCheckStatus = 1
        downCheckStatus = 0
    else:
        upCheckStatus = 0
        downCheckStatus = 1
    #print("ok")
    return

warnValue = WarnValue(0)

#串口数据

rt = Seriar()
data = ''
SerStatus = 0
SerCount = 0
SerCom = 'COM1'
dataQueue = queue.Queue(1000)
listArr = List()
file_handle = open('.1.txt', mode='w')
myFilter = Filter()
top = tk.Tk()
top.geometry('600x400')
#line
cv=tk.Canvas(top,bg='white',width=480,height=286)
cv.place(x=5, y=105, anchor=tk.NW)
cv.create_text(10, 10, text=str(warnValue.getUpValue()))
cv.create_text(10, 270, text=str(warnValue.getDownValue()))


CValue = 1
avrage = 0
RStatus = 0
def GetAvr():
    global myFilter
    global avrage
    avrage = myFilter.get()


def ReceiveTask():
    while True:
        time.sleep(0.05)
        global rt
        global data
        global CValue
        n = rt.l_serial.inWaiting()  # 获取接收到的数据长度
        if n:
            data = ((rt.l_serial.read_all().decode('utf-8')))
            #print('get data from serial port:' + data)
            if(re.search('T[0-9][0-9]=[0-9]+V',data)!=None):
                res = re.search('=[0-9]+V',data).span()
                #print(str(res))
                num = data[res[0]+1:res[1]-1]
                #print("num"+num)
                myFilter.filter(int(num))
                localtime = time.asctime(time.localtime(time.time()))
                #print("本地时间为 :", localtime)
                try:
                    file_handle.write(str(localtime)+"  "+data)
                except IOError:
                    pass
                #dataQueue.put_nowait(int(num))
                CValue = myFilter.get()
t4 = threading.Thread(target=ReceiveTask)


def openSer():
    global rt
    try:
        if  rt.start():
            rt.waiting()
        else:
            pass
    except Exception as se:
        pass

def closeSer():
    global rt
    try:
        rt.stop()
    except Exception as se:
        pass

def connectCallback():
    global SerCount
    global comB
    global rt
    global t4
    SerCount = SerCount + 1
    if(SerCount%2):
        com = comB.get()
        OpenColor.set("已打开")
        rt.setPort(com)
        openSer()
        t4.start()
    else:
        OpenColor.set("已断开")
        closeSer

def Upavlue10CallBack():
    global upCheckStatus,downCheckStatus
    if(upCheckStatus ==1  and downCheckStatus == 0):
        warnValue.AddUp10()
        UpVar.set("上限:"+str(warnValue.getUpValue()))
    elif(upCheckStatus ==0  and downCheckStatus == 1):
        warnValue.AddDown10()
        DownVar.set("下限:"+str(warnValue.getDownValue()))

def Upavlue1CallBack():
    global upCheckStatus, downCheckStatus
    if(upCheckStatus ==1  and downCheckStatus == 0):
        warnValue.AddUp1()
        UpVar.set("上限:"+str(warnValue.getUpValue()))
    elif(upCheckStatus ==0  and downCheckStatus == 1):
        warnValue.AddDown1()
        DownVar.set("下限:"+str(warnValue.getDownValue()))

def Downavlue10CallBack():
    global upCheckStatus, downCheckStatus
    if(upCheckStatus ==1  and downCheckStatus == 0):
        warnValue.SubUp10()
        UpVar.set("上限:"+str(warnValue.getUpValue()))
    elif(upCheckStatus ==0  and downCheckStatus == 1):
        warnValue.SubDown10()
        DownVar.set("下限:"+str(warnValue.getDownValue()))

def Downavlue1CallBack():
    global upCheckStatus, downCheckStatus
    if(upCheckStatus ==1  and downCheckStatus == 0):
        warnValue.SubUp1()
        UpVar.set("上限:"+str(warnValue.getUpValue()))
    elif(upCheckStatus ==0  and downCheckStatus == 1):
        warnValue.SubDown1()
        DownVar.set("下限:"+str(warnValue.getDownValue()))

UpVar = tk.StringVar()
UpVar.set("上限:0")
DownVar = tk.IntVar()
DownVar.set("下限:-0")
OpenColor = tk.StringVar()
OpenColor.set("连接")

#文件
FileLabel = tk.StringVar()
FileLabel.set("日志")
logCount = 1
def logFile():
    global file_handle
    global logCount
    if(logCount%2):
        localtime = time.asctime(time.localtime(time.time()))
        filename = "日志"+str(localtime)+'.txt'
        filename = filename.replace(' ','-')
        filename = filename.replace(':', '-')
        file_handle = open(filename, mode='w')
        FileLabel.set("正常")
    else:
        file_handle.close()
        FileLabel.set("完成")
    logCount = logCount + 1


#log 图片
filename = tk.PhotoImage(file = "logo4.gif")
logo = tk.Label(top,anchor=tk.NW,image = filename)
logo.place(x=0, y=0, anchor=tk.NW)
#down1
down1B = tk.Button(top,width=6,height=1,text="-1", bg="white",command=Downavlue1CallBack)
down1B.place(x=525, y=65, anchor=tk.NW)
#up1
up1B = tk.Button(top,width=6,height=1,text="+1", bg="white",command=Upavlue1CallBack)
up1B.place(x=472, y=65, anchor=tk.NW)
#down10
down10B = tk.Button(top,width=6,height=1,text="-10", bg="white",command=Downavlue10CallBack)
down10B.place(x=400, y=65, anchor=tk.NW)
#up10
up10B = tk.Button(top,width=6,height=1,text="+10", bg="white",command=Upavlue10CallBack)
up10B.place(x=347, y=65, anchor=tk.NW)

#com
comB = tk.Entry(top, bd =5,width=8)
comB.place(x=515, y=110, anchor=tk.NW)
#open
openB = tk.Button(top,width=8,height=1,text="连接", textvariable = OpenColor,bg="white",command=connectCallback)
openB.place(x=515, y=165, anchor=tk.NW)
#close
closeB = tk.Button(top,width=8,height=1,text="日志", textvariable = FileLabel,bg="white",command=logFile)
closeB.place(x=515, y=220, anchor=tk.NW)
#save
saveB = tk.Button(top,width=8,height=1,text="保存", bg="white",command=logFile)
saveB.place(x=515, y=275, anchor=tk.NW)
#clear
clearB = tk.Button(top,width=8,height=3,text="校准", bg="white",command=GetAvr)
clearB.place(x=515, y=330, anchor=tk.NW)

#before
#nextB = tk.Button(top,width=15,height=1,text="后退", bg="white",command=helloCallBack)
#nextB.place(x=20, y=364, anchor=tk.NW)
#auto
#nextB = tk.Button(top,width=15,height=1,text="自动", bg="white",command=helloCallBack)
#nextB.place(x=180, y=364, anchor=tk.NW)
#next
#nextB = tk.Button(top,width=15,height=1,text="前进", bg="white",command=helloCallBack)
#nextB.place(x=340, y=364, anchor=tk.NW)


#upval
Upcheck = tk.Checkbutton(top, textvariable = UpVar,font=6,command =  CheckCallBack,variable = 1,onvalue = 1, offvalue = 0)
Upcheck.place(x=10, y=65, anchor=tk.NW)
#downval
Downcheck = tk.Checkbutton(top, textvariable = DownVar,font=6,command =  CheckCallBack,variable = 1,onvalue = 0, offvalue = 1)
Downcheck.place(x=180, y=65, anchor=tk.NW)



def DrawTask():
    global cv
    global avrage
    global warnValue
    while True:
        #if dataQueue.qsize() > 0:
        #CValue = dataQueue.get()
            #print("get "+str(num))
        listArr.add(CValue)
        list = listArr.get()
        i = 0
        j = 0
        mc = 0
        cv.delete(tk.ALL)
        cv.create_text(460, 10, text=str(int(CValue)))
        cv.create_text(10, 10, text=str(warnValue.getUpValue()))
        cv.create_text(10, 270, text=str(warnValue.getDownValue()))
        cv.create_line(0,143,480,143, fill='black',width = 2)
        #print("log  "+str(avrage) +" "+ str(warnValue.getUpValue())+" "+str(warnValue.getDownValue()))
        if(warnValue.getUpValue()-warnValue.getDownValue()!=0):
            list[47] = 143-(list[47] - avrage)/(warnValue.getUpValue()-warnValue.getDownValue())*143
        else:
            list[47] = 143
        while(i<470):
            cv.create_line(i,list[j] ,i+10,list[j+1],fill='blue',width = 2)  # xyxy
            i = i + 10
            j = j + 1
        time.sleep(1)



dra = threading.Thread(target=DrawTask)
dra.start()









# 进入消息循环
top.mainloop()

