import math
import random
import queue
import matplotlib.pyplot as plt


def generateTasksAndRun(n):
    summ = 0
    count = 0
    tasks = []
    
    while (count < n):
        newTask = []
        arrival = nextExponential(100)
        service = nextExponential(200)
        summ += arrival
        newTask = [summ, service, 0]
        tasks.append(newTask)    
        count += 1
        
    DES(tasks)
    

def DES(tasks):
    events = queue.PriorityQueue()
    servQ = queue.PriorityQueue()
    dequeueList = []
    queueLenDist = [0] * 100
    queueProb = [0] * 100
    maxQueue = 0
    meanQueue = 0
    server = ""
    totalTasks = len(tasks)
    state = 0
    clock = 0
    eventList = []
    finalTasks = []
    for task in tasks:
        event = [task[0], 0 , task]
        events.put(event)
        
    for elem in list(events.queue):
        eventList.append(elem)
        
    #INIT
    state = 1
    server = []
    eventList = []
    
    while (events.empty() == False):
        E = events.get()
        clock = E[0]
        
        if (state == 0):
            server = E[2]
            events.put([E[2][1], 1, E[2]])
            finalTasks.append(server)
            state = 1

        elif (state == 1):
            temp = E[2]
            wait = max(-temp[2] + clock - temp[0],0)
            server = [temp[0],temp[1],temp[2]+wait]
            events.put([server[0]+server[1]+server[2], 1, server])
            finalTasks.append(server)
            state = 2

            
        elif (state == 2 and E[1] == 1 and servQ.empty()):
            server = []
            state = 1

            
        elif (state == 2):
            dequeueList.append(E[2])     
            servQ.put(E[2])
            state = 3

            
        elif (state == 3 and E[1] == 1 and servQ.qsize() == 1):
            del dequeueList[0]       
            temp = servQ.get()
            wait = max(-temp[2] + clock - temp[0],0)
            server = [temp[0],temp[1],temp[2]+wait]
            events.put([server[0]+server[1]+server[2], 1, server])
            finalTasks.append(server)
            state = 2

            
        elif (state == 3):
            if (E[1] == 1):
                del dequeueList[0]
                temp = servQ.get()
                wait = max(-temp[2] + clock - temp[0],0)
                server = [temp[0],temp[1],temp[2]+wait]
                events.put([server[0]+server[1]+server[2], 1, server])
                finalTasks.append(server)
            else:
                if (servQ.empty() == True):
                    events.put([E[2][1], 1, E[2]])
    
                dequeueList.append(E[2])
                servQ.put(E[2])
                
            state = 3
            
        if (E[1] == 1):
            size = servQ.qsize()
            if (size < 100):
                queueLenDist[servQ.qsize()] += 1
            
        if(servQ.qsize() > maxQueue):
            maxQueue = servQ.qsize()
            
    
    ##  Queue Distribution
    queueLenDistSum = sum(queueLenDist)
    for i in range(len(queueLenDist)):
        queueProb[i] = float(queueLenDist[i]/queueLenDistSum)
        
    ##  Mean Queue Length
    for i in range(len(queueLenDist)):
        meanQueue += queueLenDist[i]*i
    meanQueue /= float(sum(queueLenDist))
        
    ##  Max Wait Time and Mean Wait Time
    maxWait = 0
    meanWait = 0
    for i in range(len(finalTasks)):
        if (finalTasks[i][2] > maxWait):
            maxWait = finalTasks[i][2]
        meanWait += finalTasks[i][2]
    meanWait /= float(totalTasks)
    
    ##  Interarrival Time
    interArr = 0.0
    for i in range(1,len(finalTasks)):
        interArr += finalTasks[totalTasks-i][0] - finalTasks[totalTasks-i-1][0]
    interArr /= float(totalTasks)
        
    ## Server Utilization
    serverUtil = 0.0
    for i in range(len(finalTasks)):
        serverUtil += finalTasks[i][1]
    serverUtil /= float(clock) * .01        
    
    ## Server Throughput
    serverThroughput = totalTasks/float(clock)
    
    ## Little's Law
    littleLaw = float(meanQueue / (float(meanWait / float(interArr))))
    
    print("Queue length dis: " + str(queueLenDist))
    print("Queue prob dist: " + str(queueProb) + "\n\n")
    
    print("Statistics:")
    print("Total execution time: " + str(clock))
    print("Max wait time: " + str(maxWait))
    print("Mean wait time: " + str(meanWait))
    print("clock: " + str(clock))
    print("Number of Tasks: " + str(totalTasks))
    print("Max queue length: " + str(maxQueue))
    print("Mean queue length: " + str(meanQueue))
    print("Mean interarrival time: " + str(interArr))
    print("Server utilization: " + str(serverUtil) + "%")
    print("Server throughput: " + str(serverThroughput) + " tasks/second")
    print("Ratio: " + str(littleLaw))

    bins = [x - 0.5 for x in range(len(queueProb))]
    bins.append(max(bins)+1.0) 
    plt.hist(range(len(queueProb)),bins,weights=queueProb,label="Expected",color='b')
    plt.title("Queue Length Distribution")
    plt.ylabel("Probability")
    plt.xlabel("Queue Length")
    plt.show()    
        

def nextExponential(lamb):
    return (-1*(math.log(random.random())) / float(lamb))