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


import sys
import tkinter as tk

from ui.controls import textentry, tableview
from database import dao
            
class Program:

    def __init__(self, title : str):
        self.__db = dao.BooksDAO()
        self.__setupUi(title)

    def __setupUi(self, title):
        
        # MainWindow
        self.__window = tk.Tk()
        self.__window.geometry("500x250")
        self.__window.resizable(0,0)
        self.__window.title(title);
        self.__frmTop = tk.Frame(self.__window)
        self.__frmTop.pack(side=tk.TOP)
        self.__frmBottom = tk.Frame(self.__window)
        self.__frmBottom.pack(side=tk.BOTTOM)
        self.__frmBottomRight = tk.Frame(self.__window)
        self.__frmBottomRight.pack(side=tk.RIGHT, padx=10, pady=10)
        self.__frmBottomLeft = tk.Frame(self.__window)
        self.__frmBottomLeft.pack(side=tk.RIGHT, pady=10)

        # Labels
        tk.Label(self.__frmTop, text='Title').grid(row=0, column=1,padx=15)
        tk.Label(self.__frmTop, text='Year').grid(row=1, column=1,padx=15)
        tk.Label(self.__frmTop, text='Author').grid(row=0, column=3,padx=15)
        tk.Label(self.__frmTop, text='ISBN').grid(row=1, column=3,padx=15)

        # Entries
        self.__txtTitle = textentry.TextEntry(self.__frmTop, width=25)
        self.__txtTitle.grid(row=0, column=2, padx=15)
        self.__txtYear = textentry.TextEntry(self.__frmTop, width=25)
        self.__txtYear.setEntryType(int)
        self.__txtYear.grid(row=1, column=2, padx=15)
        self.__txtAuthor = textentry.TextEntry(self.__frmTop, width=25)
        self.__txtAuthor.grid(row=0, column=4, padx=15)
        self.__txtISBN = textentry.TextEntry(self.__frmTop, width=25)
        self.__txtISBN.grid(row=1, column=4, padx=15)
        self.__txtISBN.setEntryType(int)

        # DataGrid   
        self.__cols = ('ID','Title', 'Author', 'Year','ISBN')

        self.__tableView = tableview.TableView(self.__frmBottomLeft, columns=self.__cols, show='headings')
        self.__tableView.bind('<<TreeviewSelect>>', self.__tableViewSelect_Command)
        for col in self.__cols:
            self.__tableView.heading(col, text=col)
            self.__tableView.column(col, width=73, stretch=tk.NO)
        self.__tableView.pack(padx=10)

        # Buttons
        self.__btnViewAll = tk.Button(self.__frmBottomRight, text='View All',width=15, command=lambda: self.__btnViewAll_Command(None)).grid(row=0, column=0,pady=1)
        self.__btnSearchEntry = tk.Button(self.__frmBottomRight, text='Search Entry',width=15, command=lambda: self.__btnSearchEntry_Command(None)).grid(row=1, column=0,pady=1)
        self.__btnAddEntry = tk.Button(self.__frmBottomRight, text='Add Entry',width=15, command=lambda: self.__btnAddEntry_Command(None))
        self.__btnAddEntry.grid(row=2, column=0,pady=1)
        self.__btnUpdateEntry = tk.Button(self.__frmBottomRight, text='Update Selected', state=tk.DISABLED,width=15, command=lambda: self.__btnUpdateSelected_Command(None))
        self.__btnUpdateEntry.grid(row=3, column=0,pady=1)
        self.__btnDeleteEntry = tk.Button(self.__frmBottomRight, text='Delete Selected', state=tk.DISABLED,command=lambda: self.__btnDeleteSelected_Command(None),width=15)
        self.__btnDeleteEntry.grid(row=4, column=0,pady=1)
        self.__btnClose = tk.Button(self.__frmBottomRight, text='Close',width=15, command=lambda: self.__btnClose_Command(None))
        self.__btnClose.grid(row=5, column=0,pady=1)
         

    def __btnViewAll_Command(self, Object):
        allBooks = self.__db.getAllBooks()
        self.__clearAllFields()
        self.__tableView.clear()
        self.__btnAddEntry.configure(state=tk.NORMAL)
        self.__btnDeleteEntry.configure(state=tk.DISABLED)
        self.__btnUpdateEntry.configure(state=tk.DISABLED)
        self.__tableView.addItems(allBooks)
                    
    def __tableViewSelect_Command(self, Object):
         values = self.__tableView.getSelectedItem()
         self.__txtTitle.setText(values[1])
         self.__txtAuthor.setText(values[2])
         self.__txtYear.setText(values[3])
         self.__txtISBN.setText(values[4])
         
         self.__btnAddEntry.configure(state=tk.DISABLED)
         self.__btnDeleteEntry.configure(state=tk.NORMAL)
         self.__btnUpdateEntry.configure(state=tk.NORMAL)


    def __btnSearchEntry_Command(self, Object):
        self.__tableView.clear()
        
        title = self.__txtTitle.get()
        author = self.__txtAuthor.get()
        
        year = int(self.__txtYear.get()) 
        isbn = int(self.__txtISBN.get())

        records = self.__db.searchForBook(title, author, year, isbn)
        self.__tableView.addItems(records)

    def __btnAddEntry_Command(self, Object):
        if (self.__validateTextInputs()):
            title = self.__txtTitle.get()
            author = self.__txtAuthor.get()
            year = int(self.__txtYear.get())
            isbn = int(self.__txtISBN.get())
            self.__db.addBookEntry(title, author, year, isbn)
            self.__btnViewAll_Command(None)
        
    def __btnUpdateSelected_Command(self, Object):
        if (self.__validateTextInputs()):
            book_id = int(self.__tableView.getSelectedItem[0])
            self.__db.updateBookEntry(book_id, self.__txtTitle.get(), self.__txtAuthor.get(), int(self.__txtYear.get()), int(self.__txtISBN.get()))
            self.__btnViewAll_Command(None)

    def __btnDeleteSelected_Command(self, Object):
        selected = self.__tableView.getSelectedItem()
        if selected:
            book_id = selected[0]
            self.__db.deleteBookEntry(book_id)
            self.__btnViewAll_Command(None)


    def __btnClose_Command(self, Object):
        self.__window.destroy()

        
    def __validateTextInputs(self):
        for widget in self.__frmTop.winfo_children():
            if isinstance(widget,textentry.TextEntry):
                if (not widget.validate()):
                    return False
        return True


    def __clearAllFields(self):
        for widget in self.__frmTop.winfo_children():
            if isinstance(widget,textentry.TextEntry):
                widget.clear()
 
    
if __name__ == '__main__':
    Program("Library Management System")
