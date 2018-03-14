from simplequeue import SimpleQueFromEmail
from consumer import  Consumer

# ------------------------------------------------------------
if __name__ == "__main__":

    sq = SimpleQue()
    sq.configure("que", create_dir=False)
    if not sq.configured:
        print(f"Problem with configuration: {sq.err_message}")
        exit()

    consumer = Consumer()

    consumer.setInputQueue(sq)
    consumer.pop_messages()
