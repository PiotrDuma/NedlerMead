from main import func
from copy import copy
from math import *
import random
#bibliography: 
#https://www.researchgate.net/publication/250889865_Effect_of_dimensionality_on_the_Nelder-Mead_simplex_method
#http://optymalizacja.w8.pl/simplexNM.html
#http://www.kmg.zut.edu.pl/opt/wyklad/bezgrad/simplex.html
class NelderMead(object):


    def __init__(self, equation,maxIter = 100, eps = 0.001, alfa1= 1,beta1=0.5,gamma1=2):
        self.function=equation
        self.maxIteration = maxIter
        self.epsilon = eps
        self.alfa= alfa1
        self.beta= beta1
        self.gamma= gamma1
        
        self.DATA = []
        self.HISTORY = []
 
        
    def runSimplex(self,startPoint, epsilon, dim):
        
        self.iterator = 0
        
        #init first tuple object
        prevBest = func(self.function, startPoint)
        self.DATA.append([startPoint, prevBest])
        
        #init simplex points
        #create +n(dim) points with every val+initLength
        for i in range(dim): 
            buff = copy(startPoint)
            buff[i] = buff[i] + random.uniform(1,3)
            buffVal = func(self.function, buff)
            self.DATA.append([buff,buffVal])
        print(self.DATA)
        self.HISTORY = copy(self.DATA)
        stopReq = self.chceckRequest(self.iterator)
#         stopReq = True
        ###  START ITERATIONS  ###  
        while(stopReq):
            self.iterator = self.iterator+1
            #sort simplex for best(lowest) value at the start   
            self.sortSimplex()
            
            centroid = self.centroid(func,dim) #centre of simplex    
            reflection = self.reflection(func, centroid)
            
            if(reflection[1] < self.DATA[0][1]): #Fr < min
                expansion = self.expansion(func, reflection, centroid)
                if(expansion[1] < self.DATA[-1][1]): #Fe < max
                    self.DATA[-1] = expansion
                else:
                    self.DATA[-1] = reflection #next iteration if not F0>min
            
            if(reflection[1] > self.DATA[0][1]):
                for i in self.DATA[:-1]:
                    if(reflection[1] >= self.DATA[-1][1]):
                        continue
                    else:
                        self.DATA[-1]= reflection
                        
                contraction = self.contraction(func, centroid)
                if(contraction[1] >= self.DATA[-1][1]):
                    self.reduction()
                else:
                    self.DATA[-1] = contraction
                    
                for i in self.DATA[:-1]:
                    if(reflection[1] < self.DATA[-1][1]):
                        self.DATA[-1] = reflection
            #check iteration request
            stopReq = self.chceckRequest(self.iterator)
            self.HISTORY.append(self.DATA[-1])
            #END OF WHILE ITERATION

        print("Loops:  ", self.iterator)
        self.sortSimplex()    
        print(self.DATA)
        print("ERROR:  ",self.returnErr())
           
#############################################

    def centroid(self, f ,dim):                 
        centroid = [0]*dim
#         for i in range(dim):#iter through whole DATA without maxval
        for i in self.DATA[:-1]:
            buff= i[0]
            for j in range(len(buff)): #iter througth n=dim
                centroid[j] = centroid[j]+(buff[j]/dim)
        val = f(self.function, centroid)
        return [centroid, val]
    
    def reflection(self,f,centroid):
        point = centroid[0] + self.alfa*(centroid[0]-self.DATA[-1][0])# -worst point of simplex
        value = f(self.function, point)
        return [point,value]
        
    def expansion(self,f,reflect,centroid):
        point = centroid[0] + self.gamma*(centroid[0]-reflect[0])
        value = f(self.function, point)
        return [point,value]    
        
    def contraction(self,f,centroid):
        point = centroid[0] + self.beta*(self.DATA[-1][0] - centroid[0])# -worst point of simplex
        value = f(self.function, point)
        return [point,value]       
    
    def reduction(self):
        for i in self.DATA[:]:
            buff= i[0]
            for j in range(len(buff)): #iter througth n=dim
                (i[0])[j] = (( (i[0])[j]) +  ((self.DATA[0][0])[j]))/2
        
    def sortSimplex(self):
        self.DATA.sort(key=lambda tup: tup[1], reverse=False)
        
    def returnErr(self):
#         err = sqrt(1/dim *sum())
        fmse = 0
        for i in self.DATA[:]:
            fmse = fmse + i[1];
        fmse = fmse*1/len(self.DATA)
        
        ferr=[0]*len(self.DATA)
        
        for i in range(len(self.DATA[:])):
            ferr[i] = (self.DATA[i][1] - fmse)**2
        
        error = sqrt(1/(len(self.DATA)-1) * fsum(ferr))
        return error
        
    def chceckRequest(self,iteration):
        if(iteration > self.maxIteration):
            return False
        else:
            if(self.returnErr() <= self.epsilon):
                return False
            else:
                return True
    def returnHistory(self):
        return self.HISTORY
    def returnIter(self):  
        return self.iterator 
    def returnDATA(self):
        return self.DATA