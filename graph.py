from csv import reader
import matplotlib
import matplotlib.patches as mpatches
from matplotlib import pyplot

with open('ErlangResults.csv', 'r') as f:
    data = list(reader(f))

with open('MT_a_results.csv', 'r') as f:
    data2 = list(reader(f))

traffic = [float(i[2]) for i in data[1::]]
GOS = [float(j[3]) for j in data[1::]]

traffic2 = [float(i[2]) for i in data2[1::]]
GOS2 = [float(j[3]) for j in data2[1::]]

pyplot.plot(traffic,GOS,'r', label='Predicted GOS',linewidth=3)
pyplot.plot(traffic2,GOS2,'b--', label='Actual GOS')

pyplot.legend()
pyplot.title('Predicted vs Actual Grade of Service')

pyplot.xlabel('Offered Traffic (Erlangs)')
pyplot.ylabel('GOS values(%)')

pyplot.xticks([0,50,100,150,200,250,300])
pyplot.yticks([0,20,40,60,80,100])
#pyplot.xticks([0,10000,20000,30000,40000])
pyplot.show()