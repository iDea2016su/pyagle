import numpy as np
import os


class DataRecord:
    def __init__(self, path, No=0, length=50):
        self.data_list = []
        self.path = path
        self.length = length
        self.No = No
        self.var = 1

    def set_path(self, path):
        if path != '':
            self.path = path
        print(self.path)

    def set_No(self, No):
        self.No = No
        print(self.No)

    def add(self, data):
        print('data add: ' + str(data))
        self.data_list.append(data)
        while len(self.data_list) > self.length:
            self.data_list.pop(0)

    def data_record(self):
        print('data record')
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            f = open(self.path + '/' + str(self.No) + '.txt', 'w')
            for item in self.data_list:
                f.writelines(str(item))
                f.write('\n')
            f.close()
        except IOError:
            return 'IOError occurred'
        else:
            ret = self.path + '/' + str(self.No) + '.txt, total' + str(len(self.data_list))
            self.No += 1
            if self.No == 72:
                self.No = 0
            self.data_list.clear()
            return ret

    def data_clear(self):
        print('data clear')
        self.data_list.clear()

    def check_var(self, var_t=0.25):
        print('data check')
        var = np.var(self.data_list)
        self.var = var
        if len(self.data_list) < self.length:
            return False
        print(var)
        if var <= var_t:
            return True
