from csv import reader
import matplotlib
import matplotlib.patches as mpatches
from matplotlib import pyplot

with open("ErlangResults.csv", 'r') as f:
    data = list(reader(f))

with open("gammaresults.csv", 'r') as f:
    data2 = list(reader(f))

with open("logresults.csv", 'r') as f:
    data3 = list(reader(f))

with open("expresults.csv", 'r') as f:
    data4 = list(reader(f))

traffic = [float(i[2]) for i in data[1::]]
GOS = [float(j[3]) for j in data[1::]]

traffic2 = [float(i[2]) for i in data2[1::]]
GOS2 = [float(j[3]) for j in data2[1::]]

traffic3 = [float(i[2]) for i in data3[1::]]
GOS3 = [float(j[3]) for j in data3[1::]]

traffic4 = [float(i[2]) for i in data4[1::]]
GOS4 = [float(j[3]) for j in data4[1::]]

pyplot.plot(traffic,GOS,'k', label='Predicted GOS',linewidth=3)
pyplot.plot(traffic2,GOS2,'b--', label='Actual GOS - Gamma')
pyplot.plot(traffic3,GOS3,'g--', label='Actual GOS - log')
pyplot.plot(traffic4,GOS4,'r--', label='Actual GOS - exp')


pyplot.legend()
pyplot.title('Predicted vs Actual Grade of Service')

pyplot.xlabel('Offered Traffic (Erlangs)')
pyplot.ylabel('GOS values(%)')

pyplot.xticks([0,50,100,150,200,250])
pyplot.yticks([0,20,40,60,80,100])
pyplot.show()