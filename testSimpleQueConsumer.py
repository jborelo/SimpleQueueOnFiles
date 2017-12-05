import simplequeue
import logging
import time

logging.basicConfig(level=logging.DEBUG)

print (__name__)

sq =  simplequeue.SimpleQue()
sq.configure("que", create_dir=False)
while True:
    ss = sq.pop()
    if  ss:
        print (ss)
#    else:
#        print ("No message")
#    time.sleep (1)

print (__file__)