class List:
    array = [0,0,0,0,0,0,0,0,\
             0,0,0,0,0,0,0,0,\
             0,0,0,0,0,0,0,0,\
             0,0,0,0,0,0,0,0,\
             0,0,0,0,0,0,0,0,\
             0,0,0,0,0,0,0,0]
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
        print(str(self.array))
        return self.array