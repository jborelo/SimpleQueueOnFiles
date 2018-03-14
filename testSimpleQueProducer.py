from simplequeue import SimpleQue
import time
import datetime
import json


# --------------------------------------------------------
def push_messages(queue, verbose=True, nb=100000, waitTime=0):
    """
    :waitTime in seconds, time between pushing
    :param queue:
    :param verbose:
    :param nb:  max number of messages to  be inserted into queue
    :return: True if all messages were sucesfully inserted into queue, or  False is et least one failed
    """
    """

    :param queue:
    
    """

    cntr = 0
    while cntr < nb:
        cntr += 1

        message = generate_message(cntr)
        if verbose:
            print(f"Pushing message: {message}")

        b = sq.push(message)

        if not b:
            print(f"Pushing message error!! : ..{sq.err_message}..")
        time.sleep(waitTime)


# --------------------------------------------------------------------
def generate_message(cnter):
    di = {}
    di[SimpleQue.KEY_CONTENT] = f"Message: {cnter}"
    dt = datetime.datetime.now()
    di[SimpleQue.KEY_TIME] = dt.__str__()
    message = json.dumps(di, indent=4, default=myconverter)
    return message


# -------------------------------------------------------------
def myconverter(o):
    """        converts datatime object to string
    :param o:
    :return: str
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()


if __name__ == "__main__":

    sq = SimpleQue()
    sq.configure("que", create_dir=True)

    if not sq.configured:
        print("Problem with configuration")
        print(sq.err_message)
        exit()

    print("Starting test")
    push_messages(sq, waitTime=1)
