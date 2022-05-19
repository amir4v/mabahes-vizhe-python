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

class TextEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entryType = str

    def setEntryType(self, entryType):
        self.__entryType = entryType

    def validate(self):
        if len(self.get()) < 1 or (self.__entryType == int and not self.get().isnumeric()):
               self.configure(bg='red')
               self.focus_set()
               return False
        self.configure(bg='white')
        return True

    def clear(self):
        self.delete(0, tk.END)

    def setText(self, text):
        self.clear()
        self.insert(0, text)
