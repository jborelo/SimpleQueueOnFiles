from simplequeue import SimpleQue
import time
import datetime
import json


class Producer:

    def setOutputQueue(self, queu):
        self.__sq__ = queu

    def push_messages(self, queue, verbose=True, nb=100000, waitTime=0):
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

            message = self.generate_message(cntr)
            if verbose:
                print(f"Pushing message: {message}")

            b = self.__sq__.push(message)

            if not b:
                print(f"Pushing message error!! : ..{self.__sq__.err_message}..")
            time.sleep(waitTime)

    def generate_message(self, cnter):
        di = {}
        di[SimpleQue.KEY_CONTENT] = f"Message: {cnter}"
        dt = datetime.datetime.now()
        di[SimpleQue.KEY_TIME] = dt.__str__()
        message = json.dumps(di, indent=4, default=Producer.myconverter)
        return message

    @staticmethod
    def myconverter(o):
        """        converts datatime object to string
        :param o:
        :return: str
        """
        if isinstance(o, datetime.datetime):
            return o.__str__()
