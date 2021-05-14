## @package CWord
#  Documentation for this module.
#
#  This module is intended to record my progress in language
#
#  CWord module contain a class which handle :
#  Database creation, fill in and data managing
#  Notice that origin means single record in database, could be :
#  Word OR Phrasal Verbs OR Idiom 

import sqlite3
import csv
import time
import CSVReader
import logging

## Documentation for a class.
#
#  Word class provide all neccessary functionalities for this module
class Word:
    """ Word constructor

    name - name of the database to connect/create
    """
    def __init__(self, name) :
        self.name = "NONE"
        if name == 'mem' :
            self.name = ':memory:'
        elif ".db" in name:
            self.name = name
        else :
            logging.warning(name + " is not .db file")
            exit
        self.tableName = "record"
        self.connDB = sqlite3.connect(str(self.name))
        self.cursorDB = self.connDB.cursor()
        self.initDB()
    
    def __del__(self) :
        """ Word destructor """
        self.closeConnection()

    def initDB(self) :
        """ Database init

        This method creates database if not exist, else - just pass.
        """
        try :
            self.cursorDB.execute("""CREATE TABLE """ + self.tableName + """ (
                originID integer,
                lectureID integer,
                origin text,
                sentence text,
                trans text,
                category text,
                dikiLink text
                )""")
            self.connDB.commit()
        except sqlite3.OperationalError:
            logging.info("Table words exist!")
        except sqlite3.DatabaseError:
            logging.warning("File is not a database")

    def getColumnNames(self) :
        """ Get column names from database

        Return list with columns name
        """
        names = ["ID", "LECTURE", "ORIGIN", "SENTENCE", "TRANSLATION", "CATEGORY", "Diki LINK"]
        return names

    def getLectureID(self) :
        """ Get last lecture, could be use for all lectures counting
        
        Return Last kecture ID
        TODO: This will return last lecture ID only when we have an increasing order in the db,
              We don't want to limit ourselfes to keep the order
        """
        with self.connDB:
            try:
                self.cursorDB.execute("SELECT lectureID FROM " + self.tableName + " ORDER BY lectureID DESC LIMIT 1")
                lectureID = self.cursorDB.fetchall()[0][0]
            except IndexError:
                # The execution will return error if DB is empty
                lectureID = 0
        return lectureID

    def getLectureProgress(self, lectureID) :
        """ Get all origins from lecture
        
        lectureID - ID of corresponding lecture
        Return number of origins
        """
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " WHERE lectureID = '" + str(lectureID) + "'")
            originList = self.cursorDB.fetchall()
            total_length = sum(len(row) for row in originList)
        except IndexError:
            total_length = 0
        return total_length

    def getLastID(self) :
        """ Get last recorded ID from database
        
        Return The highest ID from database
        """
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " ORDER BY originID DESC LIMIT 1")
            lastID = self.cursorDB.fetchall()[0][0]
        except IndexError:
            lastID = 0
        return lastID

    def getOriginID(self, origin) :
        """ Get ID of particular origin

        origin - The word for ID will be returned
        Return ID of provided origin
        """
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " WHERE origin = '" + str(origin) + "'")
            ID = self.cursorDB.fetchall()[0][0]
        except IndexError:
            ID = 0
        return ID

    def getOriginByID(self, ID) :
        """ Get origin of specified ID
        
        ID - originID
        Return origin
        """
        try:
            self.cursorDB.execute("SELECT origin FROM " + self.tableName + " WHERE originID = " + str(ID))
            origin = self.cursorDB.fetchall()[0][0]
        except IndexError:
            origin = 'N/A'
        return origin

    def getSentenceByID(self, ID) :
        """ Get origin of specified ID
        
        ID - originID
        Return sentence
        """
        try:
            self.cursorDB.execute("SELECT sentence FROM " + self.tableName + " WHERE originID = " + str(ID))
            sentence = self.cursorDB.fetchall()[0][0]
        except IndexError:
            sentence = 'N/A'
        return sentence

    def getLectureIDs(self, lectureID) :
        """ Get IDs of specified lecture
        
        lectureID - ID of the corresponding lecture
        Return IDs list
        """
        listIDs = []
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " WHERE lectureID = " + str(lectureID))
            IDs = self.cursorDB.fetchall()
            for index in range(len(IDs)) :
                listIDs.append(IDs[index][0])
        except IndexError:
            listIDs = 'N/A'
        except sqlite3.OperationalError:
            listIDs = 'N/A'
        return listIDs

    def getAllIDs(self) :
        """ Get IDs of database
    
        Return IDs list
        """
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName)
            IDs = self.cursorDB.fetchall()
        except IndexError:
            IDs = 0
        return IDs

    def getAllLectures(self) :
        """ Get lectures of database
        
        Return IDs list
        """
        try:
            self.cursorDB.execute("SELECT lectureID FROM " + self.tableName)
            IDs = self.cursorDB.fetchall()
            lectures = []
            for row in IDs :
                lectures.append(row[0]) if row[0] not in lectures else lectures
        except IndexError:
            lectures = [0]
        return lectures

    def addRecordFromCSV(self, row) :
        """ Add single row to database from CSV file
        
        row - row to add
        row format :
        [0] Lecture ID
        [1] Lecture ID
        [2] Origin
        [3] Sentence contains origin
        [4] Traslation of origin
        [5] Origin category
        """
        if self.__checkRecord(row):
            newID = self.getLastID() + 1
            if row[4] == "NULL" :
                link = "https://www.diki.pl/slownik-angielskiego?q=" + str(row[1].lower()).replace(" ", "+")
            else :
                link = "NULL"
            with self.connDB:
                self.cursorDB.execute("INSERT INTO " + self.tableName + " VALUES (:originID, :lectureID, :origin, :sentence, :trans, :category, :dikiLink)",
                        {'originID' :   newID,
                        'lectureID' :   row[0],
                        'origin'  :     row[1],
                        'sentence'  :   row[2],
                        'trans'  :      row[3],
                        'category'  :   row[4],
                        'dikiLink' :    link})
                logging.warning('Added record : ' + str(newID))

    def addRecord(self, row) :
        """ Add single row to database

        row - row to add
        row format :
        [0] Lecture ID
        [1] Origin
        [2] Sentence contains origin
        [3] Traslation of origin
        [4] Origin category
        """
        if self.__checkRecord(row):
            if row[4] == "NULL" :
                link = "https://www.diki.pl/slownik-angielskiego?q=" + str(row[1].lower()).replace(" ", "+")
            else :
                link = "NULL"
            with self.connDB:
                self.cursorDB.execute("INSERT INTO " + self.tableName + " VALUES (:originID, :lectureID, :origin, :sentence, :trans, :category, :dikiLink)",
                        {'originID' :   row[0],
                        'lectureID' :   row[1],
                        'origin'  :     row[2],
                        'sentence'  :   row[3],
                        'trans'  :      row[4],
                        'category'  :   row[5],
                        'dikiLink' :    link})
                logging.warning('Added record : ' + str(row[0]))

    def insertRecord(self, row) :
        """  The record can be inserted to the db

        update and adding new record should be accessible from this point
        row - row to add
        row format :
        [0] Record ID
        [1] Lecture ID
        [2] Origin
        [3] Sentence contains origin
        [4] Traslation of origin
        [5] Origin category
        """
        if row[0] == "" :
            # New element
            row[0] = str(self.getLastID() + 1)
            self.addRecord(row)
        else :
            # Updated
            self.updateRow(row)

    def insertRecords(self, data) :
        """ The records can be inserted as a list
        
        Iterate through the list and parse row further
        data - list with rows
        """
        for row in data :
            logging.debug("Row format :\n\t" + row[0] + 
                      "\n\t" + row[1] + 
                      "\n\t" + row[2] + 
                      "\n\t" + row[3] + 
                      "\n\t" + row[4] +
                      "\n\t" + row[5])
            self.insertRecord(row)

    def deleteRecords(self, data) :
        """ The records can be inserted as a list
 
        Iterate through the list and parse the ID further
        data - list with IDs to delete 
        """
        lastID = self.getLastID()
        for index in range(len(data)) :
            if int(data[index]) > int(lastID) :
                logging.debug("Nothing to delete")
            else :
                self.deleteRecord(data[index])

    def deleteRecord(self, ID) :
        """ Delete record from database

        ID - ID of record to delete
        """
        if ID != 0 :
            with self.connDB:
                try :
                    self.cursorDB.execute("DELETE FROM " + self.tableName + " WHERE originID = " + str(ID))
                    logging.debug("Deleted row : " + str(ID))
                except sqlite3.OperationalError :
                    logging.error('Element not exist!')
            self.__refreshIDs(int(ID) + 1)
        else :
            logging.error('Error! Row format : [lectureID, origin, sentence, trans, category]')

    def __refreshIDs(self, oldID) :
        """ Data could be deleted in the middle, the ID should be updated
        
        Update EVERY ID after given one to value 'ID - 1'
        oldID - ID to start with refresh
        """
        _lastID = self.getLastID() - 1 
        if oldID != _lastID :
            with self.connDB:
                try:
                    self.cursorDB.execute("""UPDATE """ + self.tableName + 
                                          """ SET  originID = originID-1""" +
                                          """ WHERE originID > :oldID""",
                                          {'oldID': oldID})
                    return True
                except IndexError:
                    logging.error("IndexError")

    def importCSV(self, filename) :
        """ Import CSV file to database
        
        filename - CSV file name to be imported
        Note that file format has to follow row format from addRecordFromCSV (use comma as a delimiter) 
        """
        tic = time.perf_counter()
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                ID = self.getOriginID(row[1])
                if ID == 0 :
                    self.addRecordFromCSV(row)
                else :
                    logging.warning(row[1] + " exist on position " + str(ID))
        toc = time.perf_counter()
        logging.info(f"Imported CSV file in {toc - tic:0.4f} seconds")

    def addSection(self, data) :
        """ Add section, format of data should be same as for addRecord()

        data - data to be added
        """
        for _row in data :
           self.addRecord(_row)
           logging.info("Added row : " + str(_row))       

    def updateSection(self, data) :
        """ Edit section in database
        
        data - entire and edited lectures data
        """
        for _row in data :
            if self.updateRow(_row) :
                logging.info("Updated row : " + str(_row))

    def updateRow(self, row) :
        """ Edit row in database

        row - row data (list)
        The row has to be in right format here
        """
        if self.__checkRecord(row):
            with self.connDB:
                try:
                    self.cursorDB.execute("""UPDATE """ + self.tableName + 
                                          """ SET  trans = :trans, """ + 
                                          """origin = :origin, """ +
                                          """category = :category, """ +
                                          """sentence = :sentence, """ +
                                          """lectureID = :lectureID """ +
                                          """ WHERE originID = :originID""",
                                          {'originID': row[0], 'lectureID': row[1], 'origin':row[2], 'sentence': row[3], 'trans':row[4], 'category': row[5]})
                    return True
                except IndexError:
                    logging.error("IndexError")
        return False

    def getRow(self, rowNumber) :
        """ Get single row
    
        rowNumber - Number of row to be returned
        """
        self.cursorDB.execute("SELECT * FROM " + self.tableName + " WHERE originID = " + str(rowNumber))
        return self.cursorDB.fetchall()

    def getRows(self, lectureID = 0) :
        """ Get rows from lecture
        
        lectureID - ID of Lecture containing the data to be returned
        NOTE: If not specified, return data from entire database
        """
        elements = ""
        if (lectureID != 0) :
            elements = " WHERE lectureID = " + str(lectureID)
        self.cursorDB.execute("SELECT * FROM " + self.tableName + elements)
        return self.cursorDB.fetchall()

    def present(self) :
        """ Present entire Database """
        self.cursorDB.execute("SELECT * FROM " + self.tableName)
        table = self.cursorDB.fetchall()
        return table

    def closeConnection(self) :
        """ Close connection to database """
        try :
            self.connDB.close()
            logging.info('Connection to ' + self.name + ' closed!')
        except AttributeError:
            pass

    def __checkRecord(self, row) :
        """ The recors has to be check formatwise,
        
        before we can add it to the database
        row - row to check
        """
        if len(row) == 6:
            if  row[0].isdigit() and \
                row[1].isdigit() and \
                not any(map(str.isdigit, row[2])) and \
                not any(map(str.isdigit, row[4])) and \
                not any(map(str.isdigit, row[5])) :
                return True
        logging.error("Wrong row format : " +
                      "\n\tID : "           + row[0])
        return False