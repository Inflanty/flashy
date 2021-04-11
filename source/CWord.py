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
    ## Word constructor
    #  @param Name of the database to connect/create
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
    
    ## Word destructor
    def __del__(self) :
        self.closeConnection()

    ## Database init
    #  @brief This method creates database if not exist,
    #         else, just pass.
    def initDB(self) :
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

    ## Get column names from database
    #  @return list with columns name
    def getColumnNames(self) :
        #self.cursorDB.execute("SELECT * FROM record")
        #colnames = self.cursorDB.description
        #for row in colnames:
            # names.append(row[0])
        names = ["ID", "LECTURE", "ORIGIN", "SENTENCE", "TRANSLATION", "CATEGORY", "Diki LINK"]
        return names

    ## Get last lecture, could be use for all lectures counting
    #  @return Last kecture ID
    #  TODO: This will return last lecture ID only when we have an increasing order in the db,
    #        We don't want to limit ourselfes to keep the order
    def getLectureID(self) :
        with self.connDB:
            try:
                self.cursorDB.execute("SELECT lectureID FROM " + self.tableName + " ORDER BY lectureID DESC LIMIT 1")
                lectureID = self.cursorDB.fetchall()[0][0]
            except IndexError:
                # The execution will return error if DB is empty
                lectureID = 0
        return lectureID

    ## Get all origins from lecture
    #  @param lectureID
    #  @return number of origins
    def getLectureProgress(self, lectureID) :
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " WHERE lectureID = '" + str(lectureID) + "'")
            originList = self.cursorDB.fetchall()
            total_length = sum(len(row) for row in originList)
        except IndexError:
            total_length = 0
        return total_length

    ## Get last recorded ID from database
    #  @return The highest ID from database
    def getLastID(self) :
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " ORDER BY originID DESC LIMIT 1")
            lastID = self.cursorDB.fetchall()[0][0]
        except IndexError:
            lastID = 0
        return lastID

    ## Get ID of particular origin
    #  @param origin
    #  @return ID of provided origin
    def getOriginID(self, origin) :
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " WHERE origin = '" + str(origin) + "'")
            ID = self.cursorDB.fetchall()[0][0]
        except IndexError:
            ID = 0
        return ID

    ## Get origin of specified ID
    #  @param ID originID
    #  @return origin
    def getOriginByID(self, ID) :
        try:
            self.cursorDB.execute("SELECT origin FROM " + self.tableName + " WHERE originID = " + str(ID))
            origin = self.cursorDB.fetchall()[0][0]
        except IndexError:
            origin = 'N/A'
        return origin

    def getTransByID(self, ID) :
        try:
            self.cursorDB.execute("SELECT trans FROM " + self.tableName + " WHERE originID = " + str(ID))
            trans = self.cursorDB.fetchall()[0][0]
        except IndexError:
            trans = 'N/A'
        return trans  

    ## Get origin of specified ID
    #  @param ID originID
    #  @return sentence
    def getSentenceByID(self, ID) :
        try:
            self.cursorDB.execute("SELECT sentence FROM " + self.tableName + " WHERE originID = " + str(ID))
            sentence = self.cursorDB.fetchall()[0][0]
        except IndexError:
            sentence = 'N/A'
        return sentence

    ## Get IDs of specified lecture
    #  @param lectureID
    #  @return IDs list
    def getLectureIDs(self, lectureID) :
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

    ## Get IDs of database
    #  @return IDs list
    def getAllIDs(self) :
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName)
            IDs = self.cursorDB.fetchall()
        except IndexError:
            IDs = 0
        return IDs

    ## Get lectures of database
    #  @return IDs list
    def getAllLectures(self) :
        try:
            self.cursorDB.execute("SELECT lectureID FROM " + self.tableName)
            IDs = self.cursorDB.fetchall()
            lectures = []
            for lecture in range(len(IDs)) :
                if lecture not in lectures :
                   lectures.append(lecture)
        except IndexError:
            lectures = [0]
        return lectures

    ## Add single row to database
    #  @param row to add
    #         row format :
    #         [0] Lecture ID
    #         [1] Origin
    #         [2] Sentence contains origin
    #         [3] Traslation of origin
    #         [4] Origin category
    def addRecord(self, row) :
        if self.__checkRecord(row):
            newID = self.getLastID() + 1
            if newID != row[0] :
                logging.warning("Element has wrong ID : " + row[0])
            if row[4] == "NULL" :
                link = "https://www.diki.pl/slownik-angielskiego?q=" + str(row[1].lower()).replace(" ", "+")
            else :
                link = "NULL"
            with self.connDB:
                self.cursorDB.execute("INSERT INTO " + self.tableName + " VALUES (:originID, :lectureID, :origin, :sentence, :trans, :category, :dikiLink)",
                        {'originID' : newID,
                        'lectureID' : row[1],
                        'origin'  :  row[2],
                        'sentence'  : row[3],
                        'trans'  : row[4],
                        'category'  : row[5],
                        'dikiLink' : link})
                logging.warning('Added record : ' + newID)

    ## The record can be inserted to the db
    #  @breif update and adding new record should be accessible from this point
    #  @param row to add
    #         row format :
    #         [0] Record ID
    #         [1] Lecture ID
    #         [2] Origin
    #         [3] Sentence contains origin
    #         [4] Traslation of origin
    #         [5] Origin category
    def insertRecord(self, row) :
        newID = self.getLastID()
        if newID < int(row[0]) :
            # New element
            self.addRecord(row)
        else :
            # Updated
            self.updateRow(row)

    ## The records can be inserted as a list
    #  @brief Iterate through the list and parse row further
    #  @param data - list with rows    
    def insertRecords(self, data) :
        for row in data :
            logging.debug("Row format :\n\t" + row[0] + 
                      "\n\t" + row[1] + 
                      "\n\t" + row[2] + 
                      "\n\t" + row[3] + 
                      "\n\t" + row[4] +
                      "\n\t" + row[5])
            self.insertRecord(row)

    ## The records can be inserted as a list
    #  @brief Iterate through the list and parse the ID further
    #  @param data - list with IDs to delete 
    def deleteRecords(self, data) :
        lastID = self.getLastID()
        for index in range(len(data)) :
            if data[index] > lastID :
                logging.debug("Nothing to delete")
            else :
                self.deleteRecord(data[index])

    ## Delete record from database
    #  @param ID of record to delete
    def deleteRecord(self, ID) :
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

    ## Data could be deleted in the middle, the ID should be updated
    #  @brief Update EVERY ID after given one to value 'ID - 1'
    #  @param oldID - ID to start with refresh
    def __refreshIDs(self, oldID) :
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

    ## Import CSV file to database
    #  @param filename
    #  Note that file format has to follow row format from addRecord (use comma as a delimiter) 
    def importCSV(self, filename) :
        tic = time.perf_counter()
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                ID = self.getOriginID(row[1])
                if ID == 0 :
                    self.addRecord(row)
                else :
                    logging.warning(row[1] + " exist on position " + str(ID))
        toc = time.perf_counter()
        logging.info(f"Imported CSV file in {toc - tic:0.4f} seconds")

    ## Export row to CSV file
    #  @param lectureID
    #  @param row
    #  The row has to be in right format here
    def exportCSV(self) :
        CSVReader.run()

    ## Add section, format of data should be same as for addRecord()
    #  @param data - data to be added
    def addSection(self, data) :
        for _row in data :
           self.addRecord(_row)
           logging.info("Added row : " + str(_row))       

    ## Edit section in database
    #  @param data - entire and edited lectures data
    def updateSection(self, data) :
        for _row in data :
            if self.updateRow(_row) :
                logging.info("Updated row : " + str(_row))

    ## Edit row in database
    #  @param row - row data (list)
    #  The row has to be in right format here
    def updateRow(self, row) :
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

    ## Get single row
    #  @param rowNumber - Number of row to be returned
    def getRow(self, rowNumber) :
        self.cursorDB.execute("SELECT * FROM " + self.tableName + " WHERE originID = " + str(rowNumber))
        return self.cursorDB.fetchall()

    ## Get rows from lecture
    #  @param lectureID - ID of Lecture containing the data to be returned
    #  NOTE: If not specified, return data from entire database
    def getRows(self, lectureID = 0) :
        elements = ""
        if (lectureID != 0) :
            elements = " WHERE lectureID = " + str(lectureID)
        self.cursorDB.execute("SELECT * FROM " + self.tableName + elements)
        return self.cursorDB.fetchall()

    ## Present entire Database
    def present(self) :
        self.cursorDB.execute("SELECT * FROM " + self.tableName)
        table = self.cursorDB.fetchall()
        return table

    ## Close connection to database
    def closeConnection(self) :
        try :
            self.connDB.close()
            logging.info('Connection to ' + self.name + ' closed!')
        except AttributeError:
            pass

    ## The recors has to be check formatwise,
    #  before we can add it to the database
    #  @param row to check
    def __checkRecord(self, row) :
        if (len(row) == 6) and not ("#" in row[0]):
            if  row[0].isdigit() and \
                row[1].isdigit() and \
                not any(map(str.isdigit, row[2])) and \
                not any(map(str.isdigit, row[4])) and \
                not any(map(str.isdigit, row[5])) :
                return True
        logging.error("Wrong row format : " +
                      "\n\tID : "           + row[0])
        return False
