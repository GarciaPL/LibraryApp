import pandas as pd
from app import db, create_app
from app.db.models import Book

app = create_app()


def load_inventory(csv_path):
    df = pd.read_csv(csv_path, header=0, skip_blank_lines=True)

    with app.app_context():
        db.session.query(Book).delete()
        db.session.commit()

        books = []
        for _, row in df.iterrows():
            print(f"Row {row=}")
            book = Book(
                book_id=row["Id"],
                isbn=row["ISBN"],
                authors=row["Authors"],
                publication_year=int(row["Publication Year"]),
                title=row["Title"],
                language=row["Language"],
            )
            books.append(book)

        db.session.add_all(books)
        db.session.commit()
        print(f"Inserted {len(df)} book into the database.")
