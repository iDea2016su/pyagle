class WarnValue:
    upValue = 0.0
    downValue = 0.0
    averageValue = 0.0

    def __init__(self, avr):
        self.upValue = 13
        self.downValue = -13
        self.averageValue = avr

    def AddUp10(self):
        self.upValue = self.upValue + 1.0
        return

    def AddUp1(self):
        self.upValue = self.upValue + 0.1
        return

    def SubUp10(self):
        self.upValue = self.upValue - 1.0
        return

    def SubUp1(self):
        self.upValue = self.upValue - 0.1
        return

    def AddDown10(self):
        self.downValue = self.downValue + 1.0
        return

    def AddDown1(self):
        self.downValue = self.downValue + 0.1
        return

    def SubDown10(self):
        self.downValue = self.downValue - 1.0
        return

    def SubDown1(self):
        self.downValue = self.downValue - 0.1
        return

    def getUpValue(self):
        return round(self.upValue, 3)

    def getDownValue(self):
        return round(self.downValue, 3)
