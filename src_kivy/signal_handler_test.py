import signal
import sys
import time

def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C!')
    # print(signal) # Value is 2 for CTRL + C
    # print(frame) # Where your execution of program is at moment - the Line Number
    sys.exit(0)

#Assign Handler Function
signal.signal(signal.SIGINT, signal_handler)

# Simple Time Loop of 5 Seconds
secondsCount = 5
print('Press Ctrl+C in next '+str(secondsCount))
timeLoopRun = True 
while timeLoopRun:  
    time.sleep(1)
    if secondsCount < 1:
        timeLoopRun = False
    print('Closing in '+ str(secondsCount)+ ' seconds')
    secondsCount = secondsCount - 1

