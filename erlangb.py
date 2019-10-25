import math

def calculateEB(N,A0):
    temp=0
    if N == 0:
        return 1.0
    else:
        temp=calculateEB(N-1,A0)
        erlangB=(A0 * temp)/float(N + (A0 * temp))
        return erlangB

def calculateOT(numCalls):
    #calulate traffic values in erlang
    #assumes average call duration of 4 minutes 44 seconds
    avgDuration = (1.2073*29.6121)/3600
    return numCalls*avgDuration


if __name__ == '__main__':
  numChannels=30
  for calls in range(0,2000,100):   
    traffic=calculateOT(calls)
    erlangB=calculateEB(numChannels,traffic)
    gos=erlangB*100  
    print("Grade of Service for ", calls, " per hour: ",gos)     
                




    



