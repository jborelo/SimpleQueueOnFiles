from simplequeue import SimpleQue
from producer import Producer


if __name__ == "__main__":

    # do wymiany przygotowywanie kolejki
    sq = SimpleQue()
    sq.configure("que", create_dir=True)
    if not sq.configured:
        print("Problem with configuration")
        print(sq.err_message)
        exit()


    producer = Producer()
    producer.setOutputQueue(sq)


    print("Starting test")
    producer.push_messages(sq, waitTime=1)
