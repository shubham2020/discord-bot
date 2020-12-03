#!/usr/bin/env python3

import sqlite3

class Database:
    
    def __init__(self):

        self.db = sqlite3.connect('main.sqlite')
        self.cursor = self.db.cursor()
    
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

    def insertUser(self,user_id, name):
        if self.getUser(user_id):
            return
        self.cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)",(user_id, name))
        self.db.commit()

    def insertSearchQuery(self, search_text, user_id):
        if self.getSearchHistory(user_id, search_text):
            return
        self.cursor.execute("INSERT INTO search_history (search_text, user_id) VALUES (?, ?)",(search_text, user_id))
        self.db.commit()

    def getUser(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = {}".format(user_id))
        result = self.cursor.fetchone()
        return result
        
    def getSearchHistory(self, user_id, like_text):
        self.cursor.execute("SELECT search_text FROM search_history WHERE user_id = ? and search_text LIKE ? OR search_text LIKE ? OR search_text LIKE ? OR search_text = ?",(user_id, '%'+like_text+'%', '%'+like_text, like_text+'%', like_text))
        result = self.cursor.fetchall()
        return result

    def closeConnection(self):
        self.db.close()

if __name__=='__main__':
    db = Database()
    db.createTables()
    db.insertUser('1234', 'shubham')
    db.insertSearchQuery('Some NodeJs One', '1234')
    db.insertSearchQuery('Django', '1234')
    print(db.getSearchHistory('1234', 'NodeJs'))
    db.closeConnection()