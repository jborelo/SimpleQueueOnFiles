import tempfile
import os
import logging
from datetime import datetime

# ------------------------------------------
# V 2.0  - finally works..
# -------------------------------------------

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------------
# noinspection PyBroadException
class SimpleQue(object):
    __FILEMODE__ = 'a'
    __TESTFILEPREF__ = "test"   # prefix of files which are being used in  checking created queue
    __ver__ = "2.0"

    # -----------------------------------------------------------------
    def __init__(self):
        """ members are configured by config() method"""
        self.dirMessages = ""   # directory where files (messages) are stored
        self.filesExt = ""      # names extention of message files
        self.err_message = ""   # last error  message
        self.bad_files = []  # contains names of problematic files which could not be processed  previously
        self.configured = False  # set to True when configuration was done sucesfully

    # -----------------------------------------------------------
    @staticmethod
    def __to_fixlen_str__(intval, strlen):
        """
        Performs to string operation  ensuring  fixlenght output
        :param intval: value to  be converted to str
        :param strlen:  required len of str
        :return:  string eg "tostr(12, 4)  -> "0012"
        """
        return str(intval).zfill(strlen)

    # -----------------------------------------------------------
    @staticmethod
    def __generate_file_prefix__():
        """
        Based  on currrent time generates string yyyy.mm.dd.h.minute.sec.micros:
        exaampl: 2018.03.16.09.04.40.0768545_90r85ur8
        :return: String
        """
        dt = datetime.now()
        r = '.'.join([str(i).zfill(2) for i in
                      [dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
                       SimpleQue.__to_fixlen_str__(dt.microsecond, 7)]])
        return r

    # ---------------------------------------------------------------------------------------------------------
    def configure(self, dir_messages_name, create_dir=False, files_extention=".sq"):
        """

        :param dir_messages_name: full name of path to store messages
        :param create_dir:  should create or fail if not exists
        :param files_extention:  we  can have several types of messages (topics)
        :return:  True if  queue was configured, else False
        """

        # __check__ if  message dir exists (try to create)
        if not os.path.exists(dir_messages_name):
            if not create_dir:
                self.err_message = "Directory " + dir_messages_name + "  does not exist"
                logger.error(self.err_message)
                return False

            # try to  create  dir
            try:
                os.mkdir(dir_messages_name)
            except Exception as exc:
                self.err_message = f"Can not create dir: {dir_messages_name} {exc.__cause__}"
                logger.error(self.err_message)
                return False

        # dir exists if here
        self.dirMessages = dir_messages_name
        self.filesExt = files_extention

        self.configured = self.__check__()

        return self.configured

    # -------------------------------------------
    def push(self, message):
        """
        stores given message in que
        creates text file containing that message

        :param message:  string,  message to  be added to queue
        :return:  False if failed
        """

        if not self.configured:
            logger.error(f"queue not configured! :  {self.err_message}")
            return False

        file_name_prefix = SimpleQue.__generate_file_prefix__() + "_"

        try:
            # create message file
            fi = tempfile.NamedTemporaryFile(mode=SimpleQue.__FILEMODE__,
                                             dir=self.dirMessages,
                                             prefix=file_name_prefix,
                                             suffix=self.filesExt,
                                             delete=False  # keep file after creartion
                                             )
            fi.write(str(message))
            fi.close()
        except Exception as exc:
            self.err_message = "Can not create or  write message file: " + file_name_prefix + f"  ({exc.__class__})"
            logger.error("Push failed! " + self.err_message)
            return False

        return True

    # ----------------------------------------------------
    def pop(self):
        """
            returns content of oldest available message
            if no message available return empy string
            in case of error return None
            removes that message from queue
        """

        if not self.configured:
            logger.info("Queue is not configured !!")
            return False

        # try to pop file from bad_list
        for fn in self.bad_files:
            item = self.__pop_file__(fn)
            if item:
                return item  # process only one item

        # bad_files list empty or no bad file can not be processed , try with other files

        files = self.__files_list__()
        if not len(files):
            return ""

        # takes oldest file
        oldest_file_name = min(files)
        item = self.__pop_file__(oldest_file_name)

        return item

    # --------------------------------------------------------------------
    def __pop_file__(self, short_file_name):
        """

        :param short_file_name: file name to be processed (extract, remove, return content
        :return:  file content or None
        """
        logger.debug(f"pop_file: {short_file_name}")
        ret = None
        try:
            fullfilename = os.path.join(self.dirMessages, short_file_name)

            # read content into message, and delete message file
            with open(fullfilename, mode='rb') as fi:
                item = fi.read()

            os.remove(fullfilename)

            if short_file_name in self.bad_files:
                logger.debug(f"File {short_file_name} was on bad file list, removing from that list")
                self.bad_files.remove(short_file_name)

            logger.debug("pop_file success")
            ret = item
        except Exception as exc:
            if short_file_name not in self.bad_files:
                self.bad_files.append(short_file_name)
            self.err_message = f"Exception on __pop_file__(): {str(exc)}"
            logger.error(str(exc))
            logger.exception(exc)
            ret = None

        return ret

    # ----------------------------------------
    def __files_list__(self):
        """
        generates  and returns list of short files names from queue dir
        :param self:
        :return:  list of file names (can be empty) or None in case of error
        """
        files = []
        try:
            with os.scandir(self.dirMessages) as dm:
                for entry in dm:
                    if entry.is_file() and entry.name not in self.bad_files and not entry.name.startswith(
                            '.') and not entry.name.startswith(SimpleQue.__TESTFILEPREF__):
                        files.append(entry.name)
        except Exception as ex:
            logger.error(f"Scanning queue dir error: {str(ex)}")
            files = None

        return files

    # -------------------------------------------------------
    def __check__(self):
        """
        Checks if file can be written and read to/from queue directory
        :return:
        """
        dt = datetime.now()
        mess = dt.__repr__()

        # try to create file
        try:
            fi = tempfile.NamedTemporaryFile(mode=SimpleQue.__FILEMODE__,
                                             dir=self.dirMessages,
                                             suffix=SimpleQue.__TESTFILEPREF__,
                                             prefix=SimpleQue.__TESTFILEPREF__,
                                             delete=False,
                                             )
            created_file_name = fi.name
            fi.write(str(mess))
            fi.close()
        except Exception as ex:
            self.err_message = f"write file test failed: {ex.__str__()}"
            logger.error(f"Check queue failed: {self.err_message}")
            return False

        # try to read and remove
        try:
            fi = open(created_file_name, "r")
            fc = fi.read()
            fi.close()
            os.remove(created_file_name)
        except Exception as ex:
            self.err_message = f"read file test failed: {ex.__str__()}"
            logger.error(f"Check queue failed: {self.err_message}")
            return False

        if not fc == mess:
            self.err_message = "Written does not match!"
            logger.error("Check queue failed, written  and read content differs")
            return False

        return True
