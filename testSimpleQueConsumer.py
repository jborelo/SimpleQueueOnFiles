from simplequeue import SimpleQue
import time

# logging.basicConfig(level=logging.DEBUG)

sq = SimpleQue()
sq.configure("que", create_dir=False)


if not sq.configured:
    print(f"Problem with configuration: {sq.err_message}")
    exit()

while True:
    message = sq.pop()
    if message:
        print(message)
    else:
        print("No message")
        time.sleep(5)
