import threading
import time
import serial


class Serial:
    def __init__(self, Port='11'):
        # 构造串口的属性
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = 'COM' + Port
        self.ID = None
        self.data = None

    # 定义串口等待的函数

    def setPort(self, port):
        self.port = 'COM' + port

    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
            self.alive = False
            self.stop()

    # 启动串口的函数
    def start(self):
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = 115200
        # 设置等待时间，若超出这停止等待
        self.l_serial.timeout = 2
        self.l_serial.open()
        # 判断串口是否已经打开
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

    def stop(self):
        if self.l_serial.isOpen():
            self.l_serial = None
            self.alive = False
            self.waitEnd = None
            self.port = 'COM11'
            self.ID = None
            self.data = None
            return True
        else:
            return False
