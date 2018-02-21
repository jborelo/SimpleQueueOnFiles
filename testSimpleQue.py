import simplequeue as que
import time

# create Que object
sq = que.SimpleQue()
sq.configure("que", create_dir=True)

if not sq.configured:
    print ("Problem with configuration")
    print (sq.err_message)
    exit()

cntr=0
while True:
    ss = f"Message: {cntr}"
    cntr+=1
    b = sq.push(ss)
    print (f"Pushing message: {ss} - {b}")
    time.sleep(1)
