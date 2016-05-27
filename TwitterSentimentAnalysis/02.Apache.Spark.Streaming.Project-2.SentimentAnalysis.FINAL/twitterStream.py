from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerLine2D


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords, 100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    #print counts
    noTime = len(counts)
    pos = list()
    neg = list()
    times = list()
    for i in range(0, noTime):
        if len(counts[i]) != 0:
            times.append(i)
            pos.append(counts[i][0][1])
            neg.append(counts[i][1][1])

    posLine, = plt.plot(times, pos, marker='o', label='positive')    
    negLine, = plt.plot(times, neg, marker='o', label='negative')

    plt.ylabel('Word Count')
    plt.xlabel('Time Step')

    combinedList = pos + neg

    plt.xticks(np.arange(-1, max(times)+1, 1.0))
    plt.yticks(np.arange(0, max(combinedList) + 100, 50))
    plt.legend(handler_map={posLine: HandlerLine2D(numpoints=2)}, loc = "upper left")
    plt.show()



def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    result = []
    f = open(filename, 'r')
    for line in f:
        words = line.split()
        result.append(words[0])
    f.close()
    return set(result)    

def myMapping(word, pwords, nwords):
    if word in pwords:
        return ("positive", 1)
    elif word in nwords:
        return ("negative", 1)
    else:
        return ("na", 1)        

def myRunningUpdate(value, cumulativeCount):
    if cumulativeCount is None:
       cumulativeCount = 0
    return sum(value, cumulativeCount)

def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii","ignore"))


    # Print the first ten elements of each RDD generated in this DStream to the console
    #tweets.pprint()
    words = tweets.flatMap(lambda line: line.split(" "))

    posNegPairs = words.map(lambda word: myMapping(word, pwords, nwords))
    filteredPairs = posNegPairs.filter(lambda x: x[0] != "na")
    posNegCounts = filteredPairs.reduceByKey(lambda x, y: x + y)


    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).

    cumulativeCounts = posNegCounts.updateStateByKey(myRunningUpdate)
    cumulativeCounts.pprint()    
    
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    counts = []
    posNegCounts.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    
    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)
    return counts


if __name__=="__main__":
    main()
