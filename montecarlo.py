import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from scipy.stats import uniform


class simulation():

    def __init__(self, numChannels):
        self.start_times = []
        self.call_durations = []
        self.blockedCalls = 0
        self.numChannels = numChannels

    def generateCallData(self,numCalls):

        for j in range(numCalls):
            lower_bound = 0
            upper_bound = 3600 

            #start times in seconds since start of simulation
            st = np.random.uniform(lower_bound,upper_bound,1).round(2).tolist()
            #call duration in seconds
            cd = np.random.gamma(1.2073,29.6121,1).round(2).tolist()

            self.start_times.append(st)
            self.call_durations.append(cd)
        
    def startCall():

    def endCall();



if __name__ == '__main__':
    num_simulations = 1000
    numChannels = 10
    #for i in range(num_simulations):

    numCalls = 1000
    s = simulation(numChannels)
    s.generateCallData(numCalls)
    print(s.call_durations)
                






