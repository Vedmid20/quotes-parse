from tkinter import simpledialog, messagebox
import requests, time, os, mysql.connector
from dotenv import load_dotenv


load_dotenv()


class Quote:
    def __init__(self):
        self.db_config = {
            "host": os.getenv("HOST"),
            "user": os.getenv("USER"),
            "password": os.getenv("PASSWORD"),
            "database": os.getenv("DATABASE")
        }

        self.URL = "https://api.forismatic.com/api/1.0/"
        self.PARAMS = {
            "method": "getQuote",
            "format": "json",
            "lang": "en"
        }

    def get_quote(self):
        try:
            response = requests.get(self.URL, params=self.PARAMS)
            response.raise_for_status()
            self.data = response.json()
            return self.data.get("quoteAuthor", "Unknown"), self.data.get("quoteText", "")
        except:
            return None, None

    def save(self, cursor, author, quote):
        self.query = "insert into quotes (author, quote) values (%s, %s)"
        cursor.execute(self.query, (author, quote))

    def write(self):
        with open("media/quotes.txt", "w", encoding="utf-8") as f:
            f.write(f"")
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute("select * from quotes")
        fetch = cursor.fetchall()
        for i in fetch:
            with open("media/quotes.txt", "a", encoding="utf-8") as f:
                f.write(f"{i[0]}. {i[1]} - {i[2]}\n")

        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Quotes saved to quotes.txt")

    def run(self):
        count = simpledialog.askinteger("Count", "Enter the number of quotes to fetch")
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()

        if count:
            for i in range(count):
                author, quote = self.get_quote()
                if author and quote:
                    self.save(cursor, author, quote)
                    print(f"{i + 1}. Saved: {author} - {quote[:30]}...")
                else:
                    print("Failed to fetch quote.")
                time.sleep(2)

        connection.commit()
        cursor.close()
        connection.close()
        print("Data saved successfully.")
        time.sleep(1)

    def delete(self):
        self.yn = messagebox.askyesno("Delete", "Are you sure you want to delete all quotes?")
        if self.yn == True:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("truncate table quotes")
            connection.commit()
            cursor.close()
            connection.close()
