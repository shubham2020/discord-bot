#!/usr/bin/env python3

################################################################
#         MODULE TO DEAL WITH DATABASE TRANSACTIONS
################################################################

import sqlite3

class Database:

    # initialize the database connection
    def __init__(self):

        self.db = sqlite3.connect('main.sqlite')
        self.cursor = self.db.cursor()
    
    # create the tables if the tables do not exist
    def createTables(self):

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                user_id TEXT PRIMARY KEY NOT NULL,
                username TEXT
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_text TEXT,
                user_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) 
            );
        ''')

    # insert the user data if the data does not already exist in the database
    def insertUser(self,user_id, name):
        if self.getUser(user_id):
            return
        self.cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)",(user_id, name))
        self.db.commit()

    # insert the search query if an identical query does not exist already
    def insertSearchQuery(self, search_text, user_id):
        if self.getSearchHistory(user_id, search_text):
            return
        self.cursor.execute("INSERT INTO search_history (search_text, user_id) VALUES (?, ?)",(search_text, user_id))
        self.db.commit()

    # to retrieve the user data
    def getUser(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = {}".format(user_id))
        result = self.cursor.fetchone()
        return result
    
    # get search history as per the text sent by the user
    def getSearchHistory(self, user_id, like_text):
        self.cursor.execute("SELECT search_text FROM search_history WHERE user_id = ? and search_text LIKE ? OR search_text LIKE ? OR search_text LIKE ? OR search_text = ?",(user_id, '%'+like_text+'%', '%'+like_text, like_text+'%', like_text))
        result = self.cursor.fetchall()
        return result

    # provision to terminate the connection with the database
    def closeConnection(self):
        self.db.close()


if __name__=='__main__':
    db = Database()
    db.createTables()
    # db.insertUser('1234', 'shubham')
    # db.insertSearchQuery('Some NodeJs One', '1234')
    # db.insertSearchQuery('Django', '1234')
    # print(db.getSearchHistory('234', 'NodeJs'))
    db.closeConnection()