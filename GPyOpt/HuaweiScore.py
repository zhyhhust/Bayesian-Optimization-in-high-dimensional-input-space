# -*- coding: utf-8 -*-

import numpy as np
from ScoreACP_New import Score
class HuaweiData(object):

    def __init__(self):
        
        self.xlow = np.array(
            [130, 0, 0, 15.2, 220, 0, 0, 15.2, 130, 0, 0, 13.2, 220, 0, 0, 13.2, 130, 0, 0, 15.2, 220, 0, 0, 15.2, 250, 0,
             0, 15.2, 250, 0, 0, 13.2, 250, 0, 0, 15.2, 250, 0, 0, 13.2, 240, 0, 0, 15.2, 240, 0, 0, 15.2, 60, 0, 0, 15.2,
             190, 0, 0, 15.2, 280, 0, 0, 15.2, 170, 0, 0, 13.2, 280, 0, 0, 13.2, 190, 0, 0, 15.2, 280, 0, 0, 15.2, 240, 0,
             0, 15.2, 240, 0, 0, 13.2, 130, 0, 0, 12.2, 220, 0, 0, 12.2, 240, 0, 0, 14.0, 280, 0, 0, 15.2, 280, 0, 0, 12.2,
             240, 0, 0, 12.2, 250, 0, 0, 15.2])  # variable lower bounds
        self.xup = np.array(
            [210, 15, 10, 27.2, 300, 15, 10, 27.2, 210, 15, 10, 25.2, 300, 15, 10, 25.2, 210, 15, 10, 27.2, 300, 15, 10, 27.2, 330, 15,
             10, 27.2, 330, 15, 10, 25.2, 330, 15, 10, 27.2, 330, 15, 10, 25.2, 320, 15, 10, 27.2, 320, 15, 10, 27.2, 140, 15, 10, 27.2,
             270, 15, 10, 27.2, 360, 15, 10, 27.2, 250, 15, 10, 25.2, 360, 15, 10, 25.2, 270, 15, 10, 27.2, 360, 15, 10, 27.2, 320, 15,
             10, 27.2, 320, 15, 10, 25.2, 210, 15, 10, 24.2, 300, 15, 10, 24.2, 320, 15, 10, 26.0, 360, 15, 10, 27.2, 360, 15, 10, 24.2,
             320, 15, 10, 24.2, 330, 15, 10, 27.2])
        
        self.objfunction =  Score().CalcScore
        self.dim = 112  # problem dimension
        self.domain_bounds = []
        for i in range(self.dim):
            self.domain_bounds.append({'name':'var'+str(i),'type':'continuous','domain':(self.xlow[i],self.xup[i])})


if __name__ == '__main__':
    
    Data = HuaweiData()
    bounds = []
    for i in range(Data.dim):
        bounds.append({'name':'var'+str(i),'type':'continuous','domain':(Data.xlow[i],Data.xup[i])})
    print(Data.objfunction(Data.xup))

    
    
    
    
    
    
    
    