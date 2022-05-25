"""
Copyright 2022 Reza Masoumvand

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import sqlite3

class BooksDAO:
    def __init__(self):
        self.__conn = sqlite3.connect('books.db')

    def addBookEntry(self, title, author, year, isbn):
        self.__conn.execute(f"INSERT INTO tbl_books (title, author, year, isbn) VALUES ('{title}', '{author}', {year}, {isbn})")
        self.__conn.commit()

    def searchForBook(self, title, author, year, isbn):

        sql_command = "SELECT * FROM tbl_books WHERE "

        sql_command += "title LIKE '{title}%' AND ".format(title=title) if len(title) > 0  else ""
        sql_command += " author LIKE '{author}%' AND ".format(author=author) if len(author) > 0  else ""
        sql_command += " year = {year} AND ".format(year=year) if year > 0  else ""
        sql_command += " isbn = {isbn} AND ".format(isbn=isbn) if isbn > 0  else ""

        if len(sql_command) > 30:
            return self.__conn.execute(sql_command[0 :sql_command.rindex("AND")])
        return ""

    def deleteBookEntry(self, book_id):
        self.__conn.execute(f"DELETE FROM tbl_books WHERE id = {book_id}")
        self.__conn.commit()

    def updateBookEntry(self, book_id, title, author, year, isbn):
        self.__conn.execute(f"UPDATE tbl_books SET title='{title}', author='{author}',year={year}, isbn={isbn} WHERE id = {book_id}")
        self.__conn.commit()

    def getAllBooks(self):
        return self.__conn.execute("SELECT * from tbl_books")
