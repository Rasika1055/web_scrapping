import os
from dtos.urls import LocalPathUrlsDir
from dtos.file_modes import FileModes

class JsonWriter:
    """
        Writes data to json file
    """

    def __init__(self):
        self.delimiter = "/"
        absDirPath = os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]
        absDirPath.append(LocalPathUrlsDir.RESOURCES_DIR)
        self.resources_path = self.delimiter.join(absDirPath)
        print(self.resources_path)
    
    def writeToFile(self, fileName="jobs.json", data={}):
        """
            Write json data to file
        """
        fp = open("{base_path}{delimiter}{file_name}".format(base_path=self.resources_path,delimiter=self.delimiter,file_name=fileName), FileModes.WRITE_MODE)
        fp.write(str(data))
        fp.close()
