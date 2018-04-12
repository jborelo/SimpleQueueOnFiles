from simplequeue.simplequeue import SimpleQue
from simplequeue.test.test_producer_class import Producer


# -------------------------------------------------------------
def prepareQueue():
    sq = SimpleQue()
    sq.configure("que", create_dir=True)
    if not sq.configured:
        print(f"Problem with configuration: {sq.err_message}")
        return None
    return sq


if __name__ == "__main__":

    producer = Producer()

    # do wymiany przygotowywanie kolejki
    sq = prepareQueue()
    if not sq:
        exit(1)

    producer.setOutputQueue(sq)

    print("Starting test")
    producer.push_messages(sq, waitTime=1)
