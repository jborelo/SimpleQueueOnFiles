from simplequeue import SimpleQue
import time
import datetime
import json


class Consumer:

    def setInputQueue(self, queu):
        self.__sq__ = queu

    @staticmethod
    def unpack(jsonstr_message):
        """

        :param jsonstr_message:
        :return: tuple (content, seconds, microseconds)
        """
        # extract time and content
        dtpop = datetime.datetime.now()  # time of pop
        di = json.loads(jsonstr_message)
        dtpush = Consumer.strtodatetime(di[SimpleQue.KEY_TIME])  # time of push
        diff = dtpop - dtpush
        text = di[SimpleQue.KEY_CONTENT]
        return (text, diff.seconds, diff.microseconds)

    def pop_messages(self, verbose=True, waitTime=1):
        while True:
            # get message
            message = self.__sq__.pop()

            if message:
                text, sec, microsec = Consumer.unpack(message)
                print(f"{text} - {sec}, {microsec}")
            else:
                pass
                # print("No message")
                # time.sleep(waitTime)

    @staticmethod
    def strtodatetime(text):
        return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")


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
