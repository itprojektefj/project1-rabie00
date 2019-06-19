import csv
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///books.db')
connection = engine.connect()

with open('books.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print('ISBN: {}, title {}, author {}, year {}\n'.format(row[0], row[1], row[2], row[3]))
        connection.execute('INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title, :author, :year);',
                           isbn=row[0], title=row[1], author=row[2], year=row[3])
