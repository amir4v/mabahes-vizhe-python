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



import tkinter as tk
from tkinter import ttk

class TableView(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clear(self):
        for i in self.get_children():
           self.delete(i)    

    def addItems(self, items):
        for item in items:
           self.insert("", tk.END, values=item)

    def getSelectedItem(self):
        selected = self.focus()
        return self.item(selected, 'values')
