from tkinter import *
import Database


def clear_list():
    list1.delete(0, END)


def fill_list(books):
    for book in books:
        list1.insert(END, book)


tk = Tk()
tk.geometry("800x800")
tk.title("برنامه کتابخانه با دیتابیس و تینکر")

# ===================== Labels ========================
l1 = Label(tk, text="Title")
l1.grid(row=0, column=0)

l2 = Label(tk, text="Author")
l2.grid(row=0, column=2)

l3 = Label(tk, text="Year")
l3.grid(row=1, column=0)

l4 = Label(tk, text="ISBN")
l4.grid(row=1, column=2)

# ===================== Entries ========================

title_text = StringVar()
e1 = Entry(tk, textvariable=title_text)
e1.grid(row=0, column=1)

author_text = StringVar()
e2 = Entry(tk, textvariable=author_text)
e2.grid(row=0, column=3)

year_text = StringVar()
e3 = Entry(tk, textvariable=year_text)
e3.grid(row=1, column=1)

isbn_text = StringVar()
e4 = Entry(tk, textvariable=isbn_text)
e4.grid(row=1, column=3)

list1 = Listbox(tk, width=35, height=6)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(tk)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)


def get_selected_row(event):
    global selected_book

    if len(list1.curselection()) > 0:
        index = list1.curselection()[0]
        selected_book = list1.get(index)
        # title
        e1.delete(0, END)
        e1.insert(END, selected_book[1])
        # author
        e2.delete(0, END)
        e2.insert(END, selected_book[2])
        # year
        e3.delete(0, END)
        e3.insert(END, selected_book[3])
        # isbn
        e4.delete(0, END)
        e4.insert(END, selected_book[4])


list1.bind("<<ListboxSelect>>", get_selected_row)


def view_command():
    clear_list()
    books = Database.view()
    fill_list(books)


b1 = Button(tk, text="View All", width=12, command=lambda: view_command())
b1.grid(row=2, column=3)


def search_command():
    clear_list()
    books = Database.search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    fill_list(books)


b2 = Button(tk, text="Search Entry", width=12, command=search_command)
b2.grid(row=3, column=3)


def add_command():
    Database.insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    view_command()


b3 = Button(tk, text="Add Entry", width=12, command=lambda: add_command())
b3.grid(row=4, column=3)


def update_command():
    Database.update(selected_book[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    view_command()


b4 = Button(tk, text="Update Selected", width=12, command=update_command)
b4.grid(row=5, column=3)


def delete_command():
    Database.delete(selected_book[0])
    view_command()


b5 = Button(tk, text="Delete Selected", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(tk, text="Close", width=12, command=tk.destroy)
b6.grid(row=7, column=3)

view_command()
tk.mainloop()
