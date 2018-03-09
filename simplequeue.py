import tempfile
import os
from datetime import datetime


# import logging
#
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# print (__name__)


# --------------------------------------------------------------------------------------------
class SimpleQue(object):

    def __init__(self):
        self.dirMessages = ""
        self.filesExt = ""
        self.err_message = ""
        self.bad_files = []   # contains names of problematic files which could not be read previously
        self.loggerName = ""
        self.configured = False

    # -----------------------------------------------------------
    @staticmethod
    def tostr(intval, strlen):
        """git comm


        :param intval: value to  be converted to str
        :param strlen:  required len of str
        :return:  string eg "tostr(12, 4)  -> "0012"
        """
        return str(intval).zfill(strlen)

    # -----------------------------------------------------------
    @staticmethod
    def generate_file_prefix():
        """
        Based  on currrent time generates string yyyy.mm.dd   as: 2018.02.24.03
        :return: String
        """
        dt = datetime.now()
        r = '.'.join([str(i).zfill(2) for i in
                           [dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, SimpleQue.tostr(dt.microsecond, 7)]])
        return r

    # ---------------------------------------------------------------------------------------------------------
    def configure(self, dir_messages_name, create_dir=False, files_extention=".sq", logger_nam='simpleQueue'):
        """

        :param dir_messages_name: full name of path to store messages
        :param create_dir:  should create or fail if not exists
        :param files_extention:  we  can have several types of messages (topics)
        :param logger_nam:  name of logger
        :return:  True if  queue was configured, else False
        """

        # check if  message dir exists (try to create)
        if not os.path.exists(dir_messages_name):
            if not create_dir:
                self.err_message = "Directory " + dir_messages_name + "  does not exist"
                return False

            # try to  create  dir
            try:
                os.mkdir(dir_messages_name)
            except Exception as exc:
                self.err_message = f"Can not create dir: {dir_messages_name} {exc.__cause__}"
                return False

        self.dirMessages = dir_messages_name
        self.filesExt = files_extention
        self.configured = True

        return True

    # -------------------------------------------
    def push(self, message):
        """
        stores given message in que
        creates text file containing that message

        :param message:   message to  be addrd to queue
        :return:  False if failed
        """
        if not self.configured:
            return False

        file_name_prefix = SimpleQue.generate_file_prefix() + "_"

        try:
            # create message file
            fi = tempfile.NamedTemporaryFile(mode='a', suffix=self.filesExt, delete=False, dir=self.dirMessages,
                                             prefix=file_name_prefix)
            fi.write(str(message))
            fi.flush()
            fi.close()
        except Exception as exc:
            self.err_message = "Can not create or  write message file: " + fi.name + f"  ({exc.__class__})"
            return False

        return True

    # ------------------------------------
    def clear_bad_files(self):
        """
        removes file nammes  from bad file names list
        :return:
        """
        self.bad_files.clear()

    # ------------------------------------
    def get_bad_files(self):
        """
        returns as a list content of bad_files_names
        :return: list of strings
        """
        return self.bad_files


    # ----------------------------------------------------
    def pop(self, use_bad_files_list=True):
        """
            returns content of oldest available message
            if no message available return empy string
            in case of error treturn None

            removes that message from queue
        """

        if not self.configured:
            return False

        item = ""  # item to  be returned
        try:
            files = []
            # load files names (messages to be retrieved
            with os.scandir(self.dirMessages) as dm:
                for entry in dm:
                    if not entry.name.startswith('.') and entry.is_file() and entry.name not in self.bad_files:
                        files.append(entry.name)

            if not len(files):
                return ""

            # takes oldest file
            mf = min(files)
            fullfilename = os.path.join(self.dirMessages, mf)

            # read content into message, and delete message file
            fi = open(fullfilename, mode='r')
            item = fi.read()
            fi.close()
            os.remove(fullfilename)
        except Exception as exc:
            # add file name to bad files list, to not to be blocked  on next pull
            self.bad_files.append(entry.name)
            self.err_message = f"Exception on pop: {exc.__class__}"
            return None

        return item
