from simplequeue import SimpleQue
import time
import datetime
import json

# logging.basicConfig(level=logging.DEBUG)

# -------------------------------------------------------
def unpack(jsonstr_message):
    """

    :param jsonstr_message:
    :return: tuple (content, timediff in microseconds)
    """
    # extract time and content
    dtpop = datetime.datetime.now()  # time of pop
    di = json.loads(message)
    dtpush = strtodatetime(di[SimpleQue.KEY_TIME])  # time of push
    diff = (dtpush - dtpop).microseconds
    text = di[SimpleQue.KEY_CONTENT]
    return (text, diff)


# -----------------------------------------------------
def pop_messages(sq, verbose=True, waitTime=1):
    while True:
        #get message
        message = sq.pop()

        if message:
            text, diff = unpack(message)
            print(f"{text} - {diff}")
        else:
            print("No message")
            time.sleep(waitTime)


# ----------------------------------------------------------------
def strtodatetime(text):
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")


# ------------------------------------------------------------
if __name__ == "__main__":
    sq = SimpleQue()
    sq.configure("que", create_dir=False)

    if not sq.configured:
        print(f"Problem with configuration: {sq.err_message}")
        exit()

    pop_messages(sq)

