import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerLine2D

def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    noTime = len(counts)
    pos = list()
    neg = list()
    times = list()
    for i in range(0, noTime):
        if len(counts[i]) != 0:
            times.append(i)
            pos.append(counts[i][0][1])
            neg.append(counts[i][1][1])

    #print pos
    #print neg
    #print times
    posLine, = plt.plot(times, pos, marker='o', label='positive')    
    negLine, = plt.plot(times, neg, marker='o', label='negative')

    plt.ylabel('Word Count')
    plt.xlabel('Time Step')

    combinedList = pos + neg

    plt.xticks(np.arange(-1, max(times)+1, 1.0))
    plt.yticks(np.arange(0, max(combinedList) + 100, 50))
    plt.legend(handler_map={posLine: HandlerLine2D(numpoints=2)}, loc = "upper left")
    print "Before show"
    plt.show()        
    print "after show"




counts = [[], [('positive', 128), ('negative', 76)], [('positive', 179), 
('negative', 93)], [('positive', 145), ('negative', 87)], [('positive', 148), ('negative', 76)], [('positive', 148), 
('negative', 97)], [('positive', 143), ('negative', 96)], [('positive', 152), ('negative', 101)], [('positive', 156), 
('negative', 85)], [('positive', 151), ('negative', 86)], [('positive', 159), ('negative', 91)], [('positive', 172), ('negative', 94)]]   




counts1 = [[('positive', 188), ('negative', 87)], [('positive', 128), ('negative', 76)], [('positive', 179), 
('negative', 93)], [('positive', 145), ('negative', 87)], [('positive', 148), ('negative', 76)], [('positive', 148), 
('negative', 97)], [('positive', 143), ('negative', 96)], [('positive', 152), ('negative', 101)], [('positive', 156), 
('negative', 85)], [('positive', 151), ('negative', 86)], [('positive', 159), ('negative', 91)], [('positive', 172), ('negative', 94)]]  


#make_plot(counts)
make_plot(counts1)