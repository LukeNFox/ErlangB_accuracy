import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
import time
import math
import csv
from scipy.stats import uniform


class simulation():

    def __init__(self, numChannels):
        self.dfObj = None
        self.activeCalls = 0
        self.blockedCalls = 0
        self.avgDuration = 0
        self.numChannels = numChannels


    def generateCallData(self,numCalls,a,b,u,sd,func):
        callInfo = []
        index = []
        sumDuration = 0
        for j in range(numCalls):
            lower_bound = 0
            upper_bound = 60

            #start times in seconds since start of simulation
            st = int(np.random.uniform(lower_bound,upper_bound,1))
            #call duration in seconds
            if func=='gamma':
                cd = int(np.random.gamma(a,b,1))
            if func=='log':
                cd = int(np.random.lognormal(u,sd,1))
            if func=='exp':
                cd = int(np.random.exponential(b,1)) 
            
            sumDuration = sumDuration + cd
             
            entry = [st,st+cd,False]
            callInfo.append(entry)
            index.append(j)
            
        if (sumDuration > 0):
            self.avgDuration = (sumDuration/numCalls)/60
        else: 
            self.avgDuration = 0

        self.dfObj = pd.DataFrame(callInfo, columns = ['Start Times','Finish Time','Success'], index=index).sort_values(by=['Start Times'])
        self.dfObj = self.dfObj.reset_index(drop=True)


    def simulate(self, numCalls):

        for i in range(numCalls):
            unfinished = 0
            expired = False
            # check how many succesful call before my index have finish times after my start time
            while expired == False :    
                for j in range(i - 1,-1,-1):
                    if (self.dfObj.at[j,'Finish Time'] > self.dfObj.at[i,'Start Times']) & self.dfObj.at[j,'Success'] == True:
                        unfinished+=1  
                    if unfinished >= self.numChannels:      
                        expired = True                   
                expired = True

            if unfinished >= self.numChannels:
                self.dfObj.at[i,'Success'] = False 
                self.blockedCalls+=1
            else:
                self.dfObj.at[i,'Success'] = True
      
    def getGOS(self, numCalls):
        if self.blockedCalls > 0:
            return (self.blockedCalls/numCalls)*100
        else:
            return 0


def calculateEB(N,A0):
    temp=0
    if N == 0:
        return 1.0
    else:
        temp=calculateEB(N-1,A0)
        erlangB=(A0 * temp)/float(N + (A0 * temp))
        return erlangB


def erlang(numCalls,numChannels,average):
    avgDuration = average/60 #average in hours
    traffic= (numCalls*avgDuration)
    erlangB=calculateEB(numChannels,traffic)
    gos=erlangB*100
    with open('./final_results/ErlangResults.csv', mode='a') as x:
        y = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        y.writerow([numCalls, avgDuration, traffic, gos])

def MonteCarlo(numCalls,numChannels,a,b,u,sd,func):
    num_simulations = 100
    sum_gos = 0
    sumDuration = 0
    for i in range(num_simulations):
        s = simulation(numChannels)
        s.generateCallData(numCalls,a,b,u,sd,func)
        s.simulate(numCalls)
        sum_gos = sum_gos + s.getGOS(numCalls) 
        sumDuration = sumDuration + s.avgDuration
    gos = sum_gos/num_simulations
    duration = float(sumDuration/num_simulations)
    traffic = float(numCalls*duration)
    with open('./final_results/{}results.csv'.format(func), mode='a') as x:
        y = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        y.writerow([numCalls, duration, traffic, gos])    
    

if __name__ == '__main__':
    numChannels = 30

    average=40.6
    a=1.2073
    b=average
    u=3.29
    sd=0.89

    calls=400

    for numCalls in range(0,calls,1):
        erlang(numCalls,numChannels,average)

    for numCalls in range(0,calls,10):
        MonteCarlo(numCalls,numChannels,a,b,u,sd,'gamma')

    for numCalls in range(0,calls,10):
        MonteCarlo(numCalls,numChannels,a,b,u,sd,'log')

    for numCalls in range(0,calls,10):
        MonteCarlo(numCalls,numChannels,a,b,u,sd,'exp')

                






