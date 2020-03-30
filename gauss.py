from scipy.optimize import curve_fit
import numpy as np

class Gauss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_pred = None
        self.par = None
    
    def gaus(self, x,factor,x_mean,sigma):
        return factor*np.exp(-(x-x_mean)**2/(2*sigma**2))

    
    def fit(self):
        x=self.x
        y=self.y
        n = len(x)        #the number of data
        mean = max(zip(x,y), key=lambda x: x[1])[0]                   #note this correction
        sigma = sum(y*(x-mean)**2)/n        #note this correction
        factor = np.quantile(y,0.7)
        
        self.par, _ = curve_fit(self.gaus,
                                x,
                                y,
                                p0=[factor,mean,sigma],
                                bounds=((0, 0,0),
                                        (10*max(y), n,np.inf)))
        self.y_pred = self.gaus(x,*self.par)
        return self.y_pred

    def estimate_total(self):
        
        if self.par is None:
            print("You must run fit first!")
            return
        
        _,m,s = self.par
        st = int(m-4*s)
        st = st if st > 0 else 0
        en = int(m+4*s)
        
        x_pred = np.arange(st, en)
        y_pred = self.gaus(x_pred, *self.par)
        
        return int(sum(y_pred))
