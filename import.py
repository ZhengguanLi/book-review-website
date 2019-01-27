import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title, :author, :year)", {"isbn":isbn, "title":title, "author":author, "year":int(year)})
    db.commit()

if __name__ == "__main__":
    main()