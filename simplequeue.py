import tempfile
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
print (__name__)

# --------------------------------------------------------------------------------------------
class SimpleQue:
    dirMessages = ""
    filesExt = ""
    err_message = ""
    bad_files=[]  # contains names of problematic files which could not be read previously


    def configure(self, dir_messages_name, create_dir=False, files_extention=".sq", logger_nam='simpleQueue'):
        print(__name__)
        # check if  message dir exists (try to create)
        if  not os.path.exists(dir_messages_name):
            if not create_dir:
                self.err_message = "Directory " + dir_messages_name + "  does not exist"
                return False
            else:
                # try to  create  dir
                try:
                    os.mkdir(dir_messages_name)
                except:
                    self.err_message="Can not create dir: " + dir_messages_name
                    return False

        self.dirMessages = dir_messages_name
        self.filesExt = files_extention
        return True


    def push(self, strItem):
        try:
            # prepare file name
            dt = datetime.now()
            pr = '.'.join([str(i) for i in [dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond]])
            pr += "_"

            # create message file
            fi = tempfile.NamedTemporaryFile(mode='a', suffix=self.filesExt, delete=False, dir=self.dirMessages,
                                             prefix=pr)
            fi.write(strItem)
            fi.flush()
            fi.close()
            # print("Spi")
            # time.sleep(300)
            # print("Obudzony")

        except:
            self.err_message= "Can not create or  write message file: " + fi.name
            return False

        return True


    def clearBadFiles(self):
        self.bad_files.clear()


    def pop(self, use_bad_files_list=True):
        message = ""
        try:
            files = []
            # load files names
            with os.scandir(self.dirMessages) as dm:
                for entry in dm:
                    if not entry.name.startswith('.') and entry.is_file() and not entry.name in self.bad_files:
                        files.append(entry.name)

            if not len(files):
                return ""

            # takes oldest file
            mf = min(files)
            fullfilename = os.path.join(self.dirMessages, mf)

            # read content into message, and delete message file
            fi = open(fullfilename, mode='r')
            message = fi.read()
            fi.close()
            os.remove(fullfilename)
        except:
            self.bad_files.append(entry.name)
            return ""

        return message


# --------------------------------------------------------------------------------------------

