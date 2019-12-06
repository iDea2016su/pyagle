import numpy as np
import os
import random
import copy
import matplotlib.pyplot as plt
from app.Filter import Filter


class DataTest:
    def __init__(self, data_list=[]):
        self.data_list = data_list
        self.avr_list = []
        self.var_list = []
        self.kalman_list = []
        self.split_list = []
        self.data_filter = Filter()

    def data_read(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            self.data_list = [0] * len(files)
            for file in files:
                if os.path.splitext(file)[1] == '.txt':
                    print(os.path.join(root, file))
                    f = open(os.path.join(root, file), "r", encoding="utf-8")
                    lines = f.readlines()
                    for i, item in enumerate(lines):
                        if int(os.path.splitext(file)[0]) in range(37, 48):
                            lines[i] = float(item.split(':')[1])
                        else:
                            lines[i] = float(item)
                    print(lines)
                    self.data_list[int(os.path.splitext(file)[0])] = lines
                    f.close()
        return True

    def data_split(self, n):
        self.split_list = [[]] * len(self.data_list)
        for i, item in enumerate(self.data_list):
            print(i)
            print(item)
            self.split_list[i] = []
            dpcopy_row = copy.deepcopy(item)
            random.shuffle(dpcopy_row)  # 重排序
            m = int(len(dpcopy_row) / n)
            for j in range(0, len(dpcopy_row), m):
                self.split_list[i].append(dpcopy_row[j:j + m])
        ret = []
        for i in range(0, n):
            ret_data_list = []
            for item in self.split_list:
                ret_data_list.append(item[i])
            ret.append(DataTest(ret_data_list))
        return ret

    def data_average(self):
        self.avr_list = [0] * len(self.data_list)
        self.var_list = [0] * len(self.data_list)
        for i, row in enumerate(self.data_list):
            self.avr_list[i] = np.average(row)
            self.var_list[i] = np.var(row)

    def data_kalman(self, phase):
        n = int(phase / 5)
        self.kalman_list = [0] * len(self.avr_list)
        for i, item in enumerate(self.avr_list):
            cnum = self.data_filter.filter(item)
            if i >= n:
                self.kalman_list[i - n] = cnum
            else:
                self.kalman_list[len(self.kalman_list) - n + i] = cnum

    def data_plot(self, phase=0):
        self.data_average()
        self.data_kalman(phase)
        fig = plt.figure(figsize=(15, 5))
        ax1 = fig.add_subplot(1, 3, 1)
        plt.title('average')
        ax2 = fig.add_subplot(1, 3, 2)
        plt.title('var')
        ax3 = fig.add_subplot(1, 3, 3)
        plt.title('kalman result')
        ax1.plot(range(0, 360, 5), self.avr_list)
        ax2.plot(range(0, 360, 5), self.var_list)
        ax3.plot(range(0, 360, 5), self.kalman_list)
        plt.show()

    def data_write(self, file_dir):
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        f = open(file_dir + '/avr.txt', 'w')
        for item in self.avr_list:
            f.writelines(str(item))
            f.write('\n')
        f.close()
        f = open(file_dir + '/var.txt', 'w')
        for item in self.var_list:
            f.writelines(str(item))
            f.write('\n')
        f.close()
        f = open(file_dir + '/kalman.txt', 'w')
        for item in self.kalman_list:
            f.writelines(str(item))
            f.write('\n')
        f.close()


if __name__ == '__main__':
    # dt5 = DataTest()
    # dt5.data_read('../data/SF5/BD')
    # dt5.data_plot()

    # dt6 = DataTest()
    # dt6.data_read('../data/SF6/BD')
    # dt6.data_plot(20)
    # dt6.data_write('../data/out/SF6_BD')

    # dt6_split_list = dt6.data_split(20)
    # for item in dt6_split_list:
    #     item.data_plot(25)

    dt7 = DataTest()
    dt7.data_read('../data/SF6/BD-zd2')
    dt7.data_plot(0)
    dt7.data_write('../data/out/SF6_BD-zd180')
