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
        self.numChannels = numChannels


    def generateCallData(self,numCalls,a,b):
        callInfo = []
        index = []
        for j in range(numCalls):
            lower_bound = 0
            upper_bound = 3600 

            #start times in seconds since start of simulation
            st = np.random.uniform(lower_bound,upper_bound,1)
            #call duration in seconds
            cd = np.random.gamma(a,b,1)

            #cd = np.random.lognormal(3.33,1.04,1)

            entry = [st,st+cd,False]
            callInfo.append(entry)
            index.append(j)

        self.dfObj = pd.DataFrame(callInfo, columns = ['Start Times','Finish Time','Success'], index=index).sort_values(by=['Start Times'])
        self.dfObj = self.dfObj.reset_index(drop=True)
        

    def simulate(self, numCalls):

        for i in range(numCalls):
            unfinished = 0
            expired = False
            # check how many succesful call before my index have finish times after my start time
            while expired == False :    
                for j in range(i,0,-1):
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

# def calculateOT(numCalls,a,b):
#     #calulate traffic values in erlang
#     avgDuration = (a*b)/3600
#     return numCalls*avgDuration

def erlang(numCalls,numChannels,a,b):
    avgDuration = ((a*b)/3600)
    traffic= (numCalls*avgDuration)
    erlangB=calculateEB(numChannels,traffic)
    gos=erlangB*100
    with open('ErlangResults2.csv', mode='a') as x:
        y = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        y.writerow([numCalls, avgDuration, traffic, gos])

def MonteCarlo(numCalls,numChannels,a,b):
    num_simulations = 1
    sum_gos = 0
    for i in range(num_simulations):
        s = simulation(numChannels)
        s.generateCallData(numCalls,a,b)
        s.simulate(numCalls)
        sum_gos = sum_gos + s.getGOS(numCalls)    
    gos = sum_gos/num_simulations
    with open('MT_a_results.csv', mode='a') as x:
        y = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        y.writerow([numCalls, gos])    
    

if __name__ == '__main__':

    numChannels = 30
    a=1.2073
    b=29.6121
    # for numCalls in range(0,40000,100):
    #     erlang(numCalls,numChannels,a,b)

    #for numCalls in range(2000,40000,100):
    numCalls = 1900
    MonteCarlo(numCalls,numChannels,a,b)


    # print("Erlang GOS for ", numCalls, "calls per hour: ",gos) 
    # print("average MonteCarlo GOS for ", numCalls, "calls per hour over ", num_simulations, " simulations: ",sum_gos/num_simulations) 

                






