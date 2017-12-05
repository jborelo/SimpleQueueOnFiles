import simplequeue
import logging
import time

logging.basicConfig(level=logging.DEBUG)

#logger = logging.getLogger(__name__)

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
print (__name__)

sq =  simplequeue.SimpleQue()
sq.configure("que", create_dir=True)

cntr=0
while True:
    ss = "Message: %s" % cntr
    cntr+=1
    print ("Pushing message: %s" % ss)
    sq.push(ss)
    time.sleep(1)
