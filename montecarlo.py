import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
import time
from scipy.stats import uniform


class simulation():

    def __init__(self, numChannels):
        self.dfObj = None
        self.activeCalls = 0
        self.blockedCalls = 0
        self.numChannels = numChannels


    def generateCallData(self,numCalls):
        callInfo = []
        index = []
        for j in range(numCalls):
            lower_bound = 0
            upper_bound = 3600 

            #start times in seconds since start of simulation
            st = int(np.random.uniform(lower_bound,upper_bound,1))
            #call duration in seconds
            cd = np.random.gamma(1.2073,29.6121,1)
            entry = [st,cd,False,False]
            callInfo.append(entry)
            index.append(j)

        self.dfObj = pd.DataFrame(callInfo, columns = ['Start Times','Call_Duration','Success','Completed'], index=index).sort_values(by=['Start Times'])
        self.dfObj = self.dfObj.reset_index(drop=True)
        

    def simulate(self,numCalls):

        for second in range(0,3600):
            #check if any calls start
            x = self.dfObj.loc[self.dfObj['Start Times'] == second]
            
            if x.empty == False:
                if self.activeCalls < self.numChannels: 
                    #if (self.numChannels - self.activeCalls) < x.index
                    #set success = true
                    self.dfObj.at[x.index,'Success'] = True
                    #increment active calls      
                    self.activeCalls+=len(x.index)

                else:
                    # increment blocked calls
                    self.blockedCalls+=len(x.index)
                    # complete to true
                    self.dfObj.at[x.index,'Completed'] = True

            y = self.dfObj.loc[(self.dfObj['Start Times'] < second) & (self.dfObj['Completed'] == False)]
            if y.empty == False:
                #Decrement all active calls where complete = false
                for i in y['Call_Duration']:
                    self.dfObj.at[y.index,'Call_Duration'] = i-1
                #if any duration = 0 set complete to true
                    z = self.dfObj.loc[(self.dfObj['Call_Duration'] <= 0) & (self.dfObj['Completed'] == False)]    
                    if z.empty == False:
                        self.dfObj.at[z.index,'Completed'] = True
                        self.activeCalls-=len(z.index)
            
            #print(self.dfObj, second, self.blockedCalls, self.activeCalls,"/", self.numChannels)            
    
    def getGOS(self, numCalls):
        return (self.blockedCalls/numCalls)*100
                    
            


if __name__ == '__main__':
    #num_simulations = 1000
    numChannels = 30
    #for i in range(num_simulations):

    numCalls = 1900
    s = simulation(numChannels)
    s.generateCallData(numCalls)
    s.simulate(numCalls)
    print(s.blockedCalls)
    print(s.getGOS(numCalls))

                






