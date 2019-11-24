#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
import re
import math

# 复选框状态
from dateutil.tz import win

from app.Filter import Filter
from app.Filter2 import Filter2
from app.List import List
from app.List2 import List2
from app.Seriar import Seriar
from app.WarnValue import WarnValue

upCheckStatus = 0
downCheckStatus = 1
checkCount = 0


def CheckCallBack():
    global checkCount
    global upCheckStatus
    global downCheckStatus
    checkCount = checkCount + 1
    if (checkCount % 2):
        upCheckStatus = 1
        downCheckStatus = 0
    else:
        upCheckStatus = 0
        downCheckStatus = 1
    # print("ok")
    return


warnValue = WarnValue(0)

# 串口数据

rt = Seriar()
SerStatus = 0
SerCount = 0
SerCom = 'COM11'
dataQueue = queue.Queue(1000)
listArr = List()
listArr1 = List2()
file_handle = open('.1.txt', mode='w')
myFilter = Filter()
myFilter2 = Filter2()
top = tk.Tk()
top.geometry('600x400')
top.resizable(0, 0)
# line
cv = tk.Canvas(top, bg='white', width=480, height=286)
cv.place(x=5, y=105, anchor=tk.NW)
cv.create_text(10, 10, text=str(warnValue.getUpValue()))
cv.create_text(10, 270, text=str(warnValue.getDownValue()))

CValue = 1
RStatus = 0



def ReceiveTask():
    global rt
    global dataQueue
    while True:
        time.sleep(0.05)
        n = rt.l_serial.inWaiting()  # 获取接收到的数据长度
        if n:
            data = ((rt.l_serial.read_all().decode('utf-8')))
            #print('get data from serial port:' + data)
            if (re.search('[8][0]:', data) != None):
                try:
                    res = str(data).split(":")
                except IndexError:
                    pass
                try:
                    l = len(res[2])
                    num = res[2][0:l-2]
                    num1 = res[1]
                    print(str(num)+":"+str(num1))
                except IndexError:
                    pass
                if (re.search('\-?[0-9]*', num) != None):
                    try:
                        d = [float(num),float(num1)]
                        dataQueue.put_nowait(d)
                    except ValueError:
                        pass
                #print(str(float(num)))

t4 = threading.Thread(target=ReceiveTask)


def openSer():
    global rt
    try:
        if rt.start():
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
    global top
    SerCount = SerCount + 1
    if (SerCount % 2):
        com = comB.get()
        OpenColor.set("已打开")
        rt.setPort(com)
        openSer()
        t4.start()
    else:
        OpenColor.set("已断开")
        closeSer()
        exit()
        quit()
        top.destroy()
        win.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0));


def Upavlue10CallBack():
    global upCheckStatus, downCheckStatus
    if (upCheckStatus == 1 and downCheckStatus == 0):
        warnValue.AddUp10()
        UpVar.set("上限:" + str(warnValue.getUpValue()))
    elif (upCheckStatus == 0 and downCheckStatus == 1):
        warnValue.AddDown10()
        DownVar.set("下限:" + str(warnValue.getDownValue()))


def Upavlue1CallBack():
    global upCheckStatus, downCheckStatus
    if (upCheckStatus == 1 and downCheckStatus == 0):
        warnValue.AddUp1()
        UpVar.set("上限:" + str(warnValue.getUpValue()))
    elif (upCheckStatus == 0 and downCheckStatus == 1):
        warnValue.AddDown1()
        DownVar.set("下限:" + str(warnValue.getDownValue()))


def Downavlue10CallBack():
    global upCheckStatus, downCheckStatus
    if (upCheckStatus == 1 and downCheckStatus == 0):
        warnValue.SubUp10()
        UpVar.set("上限:" + str(warnValue.getUpValue()))
    elif (upCheckStatus == 0 and downCheckStatus == 1):
        warnValue.SubDown10()
        DownVar.set("下限:" + str(warnValue.getDownValue()))


def Downavlue1CallBack():
    global upCheckStatus, downCheckStatus
    if (upCheckStatus == 1 and downCheckStatus == 0):
        warnValue.SubUp1()
        UpVar.set("上限:" + str(warnValue.getUpValue()))
    elif (upCheckStatus == 0 and downCheckStatus == 1):
        warnValue.SubDown1()
        DownVar.set("下限:" + str(warnValue.getDownValue()))


UpVar = tk.StringVar()
UpVar.set("上限:0")
DownVar = tk.IntVar()
DownVar.set("下限:-0")
OpenColor = tk.StringVar()
OpenColor.set("连接")

# 文件
FileLabel = tk.StringVar()
FileLabel.set("日志")
logCount = 1


def logFile():
    global file_handle
    global logCount
    if (logCount % 2):
        localtime = time.asctime(time.localtime(time.time()))
        filename = "日志" + str(localtime) + '.txt'
        filename = filename.replace(' ', '-')
        filename = filename.replace(':', '-')
        file_handle = open(filename, mode='w')
        FileLabel.set("正常")
    else:
        file_handle.close()
        FileLabel.set("完成")
    logCount = logCount + 1


im = b'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'
# log 图片
im = tk.PhotoImage(data=im)
logo = tk.Label(top, anchor=tk.NW, image=im)
logo.place(x=0, y=0, anchor=tk.NW)
# down1
down1B = tk.Button(top, width=6, height=1, text="-0.1", bg="white", command=Downavlue1CallBack)
down1B.place(x=525, y=65, anchor=tk.NW)
# up1
up1B = tk.Button(top, width=6, height=1, text="+0.1", bg="white", command=Upavlue1CallBack)
up1B.place(x=472, y=65, anchor=tk.NW)
# down10
down10B = tk.Button(top, width=6, height=1, text="-1", bg="white", command=Downavlue10CallBack)
down10B.place(x=400, y=65, anchor=tk.NW)
# up10
up10B = tk.Button(top, width=6, height=1, text="+1", bg="white", command=Upavlue10CallBack)
up10B.place(x=347, y=65, anchor=tk.NW)

# com
comB = tk.Entry(top, bd=5, width=8)
comB.place(x=515, y=110, anchor=tk.NW)
# open
openB = tk.Button(top, width=8, height=1, text="连接", textvariable=OpenColor, bg="white", command=connectCallback)
openB.place(x=515, y=165, anchor=tk.NW)
# close
closeB = tk.Button(top, width=8, height=1, text="日志", textvariable=FileLabel, bg="white", command=logFile)
closeB.place(x=515, y=220, anchor=tk.NW)
# save
saveB = tk.Button(top, width=8, height=1, text="保存", bg="white", command=logFile)
saveB.place(x=515, y=275, anchor=tk.NW)
# clear
clearB = tk.Button(top, width=8, height=3, text="校准", bg="white")
clearB.place(x=515, y=330, anchor=tk.NW)

# upval
Upcheck = tk.Checkbutton(top, textvariable=UpVar, font=6, command=CheckCallBack, variable=1, onvalue=1, offvalue=0)
Upcheck.place(x=10, y=65, anchor=tk.NW)
# downval
Downcheck = tk.Checkbutton(top, textvariable=DownVar, font=6, command=CheckCallBack, variable=1, onvalue=0, offvalue=1)
Downcheck.place(x=180, y=65, anchor=tk.NW)

def draline(tcv = cv,angle = 0):
    tcv.create_line(240, 150, 240+120*math.cos(angle), 150+120*math.sin(angle), fill='black', width=4)


a = 0.0;
def DrawTask():
    global cv
    global avrage
    global warnValue
    global dataQueue
    global a
    while True:
        num = dataQueue.get(timeout=10000)
        print("get " + str(num))
        #cnum = float(num)
        cn0 = myFilter.filter(float(num[0]))
        cn1 = myFilter2.filter(float(num[1]))
        #cnum = myFilter.filter(float(num))
        listArr.add(cn0)
        listArr1.add(cn1)
        list = listArr.get()
        list1 = listArr1.get()
        i = 0
        j = 0
        mc = 0
        x0 = 240
        y0 = 150
        r = 125
        r0 = 5
        cv.delete(tk.ALL)
        cv.create_oval(x0-r,y0-r,x0+r,y0+r)
        cv.create_oval(x0 - r0, y0 - r0, x0 + r0, y0 + r0)
        draline(cv,a)
        a = a + 0.01
        #cv.create_text(460, 10, text=str(int(CValue)))
        #cv.create_text(10, 10, text=str(warnValue.getUpValue()))
        #cv.create_text(10, 270, text=str(warnValue.getDownValue()))
        #cv.create_line(0, 143, 480, 143, fill='black', width=2)
        # print("log  "+str(avrage) +" "+ str(warnValue.getUpValue())+" "+str(warnValue.getDownValue()))
        #if (warnValue.getUpValue() - warnValue.getDownValue() != 0):
        #    list[47] = 143 + (list[47]) / (warnValue.getUpValue() - warnValue.getDownValue()) * 1430
        #else:
        #    list[47] = 143
        #while (i < 470):
        #    cv.create_line(i, list[j], i + 10, list[j + 1], fill='blue', width=2)  # xyxy
        #    i = i + 10
        #    j = j + 1

        #m = 0
        #n = 0
        #if (warnValue.getUpValue() - warnValue.getDownValue() != 0):
        #    list1[47] = 143 + (list1[47]) / (warnValue.getUpValue() - warnValue.getDownValue()) * 1430
        #else:
        #    list1[47] = 143
        #while (m < 470):
        #    cv.create_line(m, list1[n], m + 10, list1[n + 1], fill='red', width=2)  # xyxy
        #   m = m + 10
        #    n = n + 1

        time.sleep(0.01)


dra = threading.Thread(target=DrawTask)
dra.start()

# 进入消息循环
top.mainloop()
