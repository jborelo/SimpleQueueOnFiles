from simplequeue import SimpleQue
import time

# create Que object
sq = SimpleQue()

sq.configure("que", create_dir=True)

if not sq.configured:
    print("Problem with configuration")
    print(sq.err_message)
    exit()

# push several messages
cntr = 0
while True:
    message = f"Message: {cntr}"
    cntr += 1
    print(f"Pushing message: {message}")
    if not sq.push(message):
        print(f"ERROR !   ..{sq.err_message}..")

    time.sleep(1)
