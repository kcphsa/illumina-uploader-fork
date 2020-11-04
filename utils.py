import sqlite3, os, re
from datetime import datetime

class database:
    def __init__(self, dbInfo, queries):
        self.location = os.path.join(os.path.dirname(__file__), dbInfo["location"])
        print("DB location: ",self.location)
        self.folderTable = dbInfo["foldertable"]
        self.connection = self.initConnection()
        self.queries = queries

    def initConnection(self):
        return sqlite3.connect(self.location)

    def closeConnection(self):
        return self.connection.close()
    
    def createDb(self):
        c = self.connection.cursor()
        c.execute(self.queries["createtable"].format(self.folderTable))
        self.connection.commit()
        self.closeConnection()
        print("DB table folderinfo created!")
        exit()

    def getFolderList(self):
        '''
        Get list of folders from db that need uploading
        '''
        c = self.connection.cursor()
        c.execute(self.queries["getfolderstoupload"].format(self.folderTable, "UPLOADED"))
        result = c.fetchall()
        if result:
            return result
        else:
            print("No new files to upload")
            exit(0)

    def addToFolderList(self, folderName, folderRegex):
        '''
        Add folder to table
        '''
        if not re.match(folderRegex,folderName):
            print("Error wrong folder format, please check {}".format(folderName))
            exit(0)
        else:
            c = self.connection.cursor()
            c.execute(self.queries["checkfolderpresence"].format(self.folderTable, folderName))
            if c.fetchone() is None:
                print("Inserting Folder {}".format(folderName))
                currenttime = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
                c.execute(self.queries["insertfolder"].format(self.folderTable, folderName, "CREATED", currenttime))
                self.connection.commit()
            else:
                print("Folder Already Present {}".format(folderName))

    def destroyDb(self):
        '''
        Destroy database file
        '''
        pass

        