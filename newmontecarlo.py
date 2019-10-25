import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from datetime import time
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


    def generateCallData(self,numCalls,a,b):
        callInfo = []
        index = []
        sumDuration = 0
        for j in range(numCalls):
            lower_bound = 0
            upper_bound = 3600

            #start times in seconds since start of simulation
            st = np.random.uniform(lower_bound,upper_bound,1)
            #call duration in seconds
            cd = np.random.gamma(a,b,1)
            sumDuration = sumDuration + cd
            #cd = np.random.lognormal(3.33,1.04,1)
            #ft = s.getFinishTime(st+cd)
            entry = [st,st+cd,False]
            callInfo.append(entry)
            index.append(j)
            #print(entry)
        if (sumDuration > 0):
            self.avgDuration = (sumDuration/numCalls)/3600
        else: 
            self.avgDuration = 0

        self.dfObj = pd.DataFrame(callInfo, columns = ['Start Times','Finish Time','Success'], index=index).sort_values(by=['Start Times'])
        self.dfObj = self.dfObj.reset_index(drop=True)
        
    # def getFinishTime(self,start,finish):
        
    #     start = 



    def simulate(self, numCalls):

        #for i in range(numCalls):
        call = 0
        while call < numCalls:
            print("numCalls: ", numCalls)
            print("call: ", call)
            print("blocked: ", self.blockedCalls)
            currentStart = float(self.dfObj.at[call,'Start Times'])
            unfinished = 0
            channelsFull = False
            # check how many succesful call before my index have finish times after my start time
            while expired == False :    
                for j in range(i - 1,-1,-1):
                    if (self.dfObj.at[j,'Finish Time'] > self.dfObj.at[i,'Start Times']) & self.dfObj.at[j,'Success'] == True:
                        unfinished+=1  
                    if unfinished >= self.numChannels: 
                        
                        # self.blockedCalls+=1
                        # self.dfObj.at[i,'Success'] = False       
                        expired = True
                # self.dfObj.at[i,'Success'] = True                    
                expired = True


            if unfinished >= self.numChannels:
                self.dfObj.at[i,'Success'] = False 
                self.blockedCalls+=1

      
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


def erlang(numCalls,numChannels,a,b):
    avgDuration = (a*b)/3600 #average in hours

    traffic= (numCalls*avgDuration)
    erlangB=calculateEB(numChannels,traffic)
    gos=erlangB*100
    with open('ErlangResults.csv', mode='a') as x:
        y = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        y.writerow([numCalls, avgDuration, traffic, gos])

def MonteCarlo(numCalls,numChannels,a,b):
    num_simulations = 1
    sum_gos = 0
    sumDuration = 0
    for i in range(num_simulations):
        s = simulation(numChannels)
        s.generateCallData(numCalls,a,b)
        s.simulate(numCalls)
        sum_gos = sum_gos + s.getGOS(numCalls) 
        sumDuration = sumDuration + s.avgDuration
    gos = sum_gos/num_simulations
    duration = float(sumDuration/num_simulations)
    traffic = float(numCalls*duration)
    with open('MT_a_results.csv', mode='a') as x:
        y = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        y.writerow([numCalls, duration, traffic, gos])    
    

if __name__ == '__main__':

    numChannels = 30
    a=1.2073
    b=29.6121
    calls=30000
    for numCalls in range(0,calls,100):
        erlang(numCalls,numChannels,a,b)

    for numCalls in range(0,calls,1000):
        MonteCarlo(numCalls,numChannels,a,b)


    # print("Erlang GOS for ", numCalls, "calls per hour: ",gos) 
    # print("average MonteCarlo GOS for ", numCalls, "calls per hour over ", num_simulations, " simulations: ",sum_gos/num_simulations) 

                






