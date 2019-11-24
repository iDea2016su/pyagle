class Filter2:
    Q = 0.01
    R = 2.0
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
        return self.currentValue
    def get(self):
        return self.currentValue