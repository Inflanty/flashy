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
            self.tableName = "record"
            self.connDB = sqlite3.connect(str(self.name))
            self.cursorDB = self.connDB.cursor()
            self.initDB()
        else :
            logging.warning(name + " is not .db file")
            exit
    
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
        self.cursorDB.execute("SELECT * FROM record")
        names = []
        colnames = self.cursorDB.description
        for row in colnames:
            names.append(row[0])
        return names

    ## Get last lecture, could be use for all lectures counting
    #  @return Last kecture ID
    def getLectureID(self) :
        try:
            self.cursorDB.execute("SELECT lectureID FROM " + self.tableName + " ORDER BY lectureID DESC LIMIT 1")
            lectureID = self.cursorDB.fetchall()[0][0]
        except IndexError:
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
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName + " WHERE lectureID = " + str(lectureID))
            IDs = self.cursorDB.fetchall()
        except IndexError:
            IDs = 'N/A'
        return IDs

    ## Get IDs of database
    #  @return IDs list
    def getAllIDs(self) :
        try:
            self.cursorDB.execute("SELECT originID FROM " + self.tableName)
            IDs = self.cursorDB.fetchall()
        except IndexError:
            IDs = 'N/A'
        return IDs

    ## Add single row to database
    #  @param row to add
    #         row format :
    #         [0] Lecture ID
    #         [1] Origin
    #         [2] Sentence contains origin
    #         [3] Traslation of origin
    #         [4] Origin category
    def addRecord(self, row) :
        if (len(row) == 5) and not ("#" in row[0]):
            newID = self.getLastID() + 1
            if row[4] != "IT" :
                link = "https://www.diki.pl/slownik-angielskiego?q=" + str(row[1].lower()).replace(" ", "+")
            else :
                link = "NULL"
            with self.connDB:
                self.cursorDB.execute("INSERT INTO " + self.tableName + " VALUES (:originID, :lectureID, :origin, :sentence, :trans, :category, :dikiLink)",
                        {'originID' : newID,
                        'lectureID' : row[0],
                        'origin'  :  row[1],
                        'sentence'  : row[2],
                        'trans'  : row[3],
                        'category'  : row[4],
                        'dikiLink' : link})
            logging.info('Added record : ' + row[1])
        else :
            logging.error('Row format : [lectureID, origin, sentence, trans, category]')

    ## Delete record from database
    #  @param ID of record to delete
    def deleteRecord(self, ID) :
        if ID != 0 :
            with self.connDB:
                try :
                    self.cursorDB.execute("DELETE FROM " + self.tableName + " WHERE originID = " + str(ID))
                except sqlite3.OperationalError :
                    logging.warning('Element not exist!')
        else :
            logging.error('Error! Row format : [lectureID, origin, sentence, trans, category]')

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

    ## Edit section in database
    #  @param data - entire and edited lectures data
    def updateSection(self, data) :
        for _row in data :
            self.updateRow(_row)

    ## Edit row in database
    #  @param row - row data (list)
    #  The row has to be in right format here
    def updateRow(self, row) :
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
            except IndexError:
                logging.error("IndexError")

    ## Swow single row
    #  @param row to print
    def getRow(self, row) :
        self.cursorDB.execute("SELECT * FROM " + self.tableName + " WHERE originID = " + str(row))
        return self.cursorDB.fetchall()

    ## Swow single row
    #  @param row to print
    def get(self, lectureID = 0) :
        elements = ""
        if (lectureID != 0) :
            elements = " WHERE lectureID = " + str(lectureID)
        self.cursorDB.execute("SELECT * FROM " + self.tableName + elements)
        return self.cursorDB.fetchall()

    ## Present entire Database
    def present(self) :
        self.cursorDB.execute("SELECT * FROM " + self.tableName)
        table = self.cursorDB.fetchall()
        for i in table :
            logging.info(i)

    ## Close connection to database
    def closeConnection(self) :
        try :
            self.connDB.close()
            logging.info('Connection to ' + self.name + ' closed!')
        except AttributeError:
            pass
