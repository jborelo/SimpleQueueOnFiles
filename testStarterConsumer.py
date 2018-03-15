from simplequeue import SimpleQue
from test_consumer_class import Consumer


# -------------------------------------------------------------
def prepareQueue():
    sq = SimpleQue()
    sq.configure("que", create_dir=False)
    if not sq.configured:
        print(f"Problem with configuration: {sq.err_message}")
        return None
    return sq


if __name__ == "__main__":
    # prepare tester
    consumer = Consumer()

    # prepare queue
    queue = prepareQueue()

    #
    consumer.setInputQueue(queue)

    #  do  work
    consumer.pop_messages()
