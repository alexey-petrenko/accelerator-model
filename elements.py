import numpy as np

class AccElement:
    def __init__(self, L=0, s0=0, name=None):
        self.L  = L  # m
        self.s0 = s0  # m -- location of the element center along the beamline
        self.name = name
        self.type_name = None
        
    def M(self):
        L = self.L
        return np.matrix([
            [1, L, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, L, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])

class UniformElement(AccElement):
    def M(self, L=None):
        if L is None: L = self.L

        return np.matrix([
            [1, L, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, L, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
      
class Quadrupole(UniformElement):
    def __init__(self, *args, K1=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.K1 = K1 # 1/m^2 -- geometric strength of quadrupole
        self.type_name = "Quadrupole"

    def M(self, L=None):
        if L is None: L = self.L
        
        K1 = self.K1
        
        if K1 == 0:
            return np.matrix([
                [1, L, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, L, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]
            ])
        
        k = np.sqrt(np.abs(K1))
        
        sinkL  = np.sin(k*L)
        coskL  = np.cos(k*L)
        sinhkL = np.sinh(k*L)
        coshkL = np.cosh(k*L)

        if K1 > 0:
            return np.matrix([
                [   coskL, sinkL/k,  0,      0,     0, 0],
                [-k*sinkL, coskL,    0,      0,     0, 0],
                [    0,     0,    coshkL, sinhkL/k, 0, 0],
                [    0,     0,  k*sinhkL, coshkL,   0, 0],
                [    0,     0,       0,      0,     1, 0],
                [    0,     0,       0,      0,     0, 1]
            ])
        
        if K1 < 0:
            return np.matrix([
                [  coshkL, sinhkL/k,  0,     0,      0, 0],
                [k*sinhkL, coshkL,    0,     0,      0, 0],
                [    0,     0,      coskL, sinkL/k,  0, 0],
                [    0,     0,   -k*sinkL, coskL,    0, 0],
                [    0,     0,       0,      0,      1, 0],
                [    0,     0,       0,      0,      0, 1]
            ])
        
        return None

class Solenoid(UniformElement):
    def __init__(self, K=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.K = K # 1/m
        self.type_name = "Solenoid"

    def M(self, L=None):

        if L is None: L = self.L

        K = self.K

        if K == 0:
            return np.matrix([
                [1, L, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, L, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]
            ])


        S = np.sin(K*L)
        C = np.cos(K*L)

        return np.matrix([
            [ C**2,   (S*C)/K,  S*C,   (S**2)/K, 0, 0],
            [-K*S*C,   C**2,   -K*S**2, S*C,     0, 0],
            [-S*C,   -(S**2)/K, C**2,  (S*C)/K , 0, 0],
            [ K*S**2, -S*C,    -K*S*C,  C**2,    0, 0],
            [ 0,       0,       0,      0,       0, 0],
            [ 0,       0,       0,      0,       0, 0]
        ])

