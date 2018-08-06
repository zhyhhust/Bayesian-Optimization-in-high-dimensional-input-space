

# -*- coding: utf-8 -*-

import numpy as np

class Data(object):
    
    def __init__(self):
        self.dim = 50  # problem dimension
        self.xlow = -np.ones(self.dim)*10.0
        self.xup =  np.ones(self.dim)*10.0
        self.domain_bounds = []
        for i in range(self.dim):
            self.domain_bounds.append({'name':'var'+str(i),'type':'continuous','domain':(self.xlow[i],self.xup[i])})

    def objfunction(self,x):
        #x = np.array(list(x.values()))
        d=self.dim
        a=np.array([20.0]);b=np.array([0.2]);c=np.array([2.0*np.pi])
        f  = -a*np.exp(-b*np.sqrt(1.0/d)*np.linalg.norm(x)) \
             - np.exp(1.0/d*np.sum(np.cos(c*x))) + a + np.exp(1.0)
        return -f[0]

if __name__ == '__main__':
    data = Data()
    fvaule = data.objfunction(data.xlow)
#    fvaule = data.objfunction(**data.paramX)
    print(fvaule)

