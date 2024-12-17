from src.Quote import Quote
from tkinter import *
import tkinter.ttk as t
import mysql.connector


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Quote Generator")
        self.geometry("600x400")
        self.resizable(False, False)

        self.quote = Quote()
        self.buttons()
        self.treeview()

    def buttons(self):
        self.parse = t.Button(self, text="Parse", command=self.write)
        self.parse.place(x=100, y=20)

        self.d = t.Button(self, text="Delete all", command=self.delete)
        self.d.place(x=200, y=20)

        self.write = t.Button(self, text="Write to file", command=self.quote.write)
        self.write.place(x=300, y=20)

        self.q = t.Button(self, text="Quit", command=self.quit)
        self.q.place(x=400, y=20)

    def write(self):
        self.quote.run()
        self.show_tree()

    def delete(self):
        self.quote.delete()
        self.show_tree()

    def treeview(self):
        self.tree = t.Treeview(self, columns=("ID", "Author", "Quote"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Quote", text="Quote")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Author", width=150, anchor="w")
        self.tree.column("Quote", width=350, anchor="w")

        self.tree.place(x=20, y=60, width=560, height=300)

        self.show_tree()

    def show_tree(self):
        self.tree.delete(*self.tree.get_children())
        connection = mysql.connector.connect(**self.quote.db_config)
        cursor = connection.cursor()
        cursor.execute("select * from quotes")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=row)
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app = App()
    app.mainloop()