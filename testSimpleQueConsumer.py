import simplequeue
import time

# logging.basicConfig(level=logging.DEBUG)


sq =  simplequeue.SimpleQue()
sq.configure("que", create_dir=False)

if not sq.configured:
    print ("Problem with configuration")
    print (sq.err_message)
    exit()

while True:
    ss = sq.pop()
    if  ss:
        print (ss)
    else:
        print ("No message")
        time.sleep (1)
