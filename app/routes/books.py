from flask import request, jsonify, Blueprint
from sqlalchemy import or_

from app.db.models import Book, Wishlist, db

bp = Blueprint("books", __name__, url_prefix="/v1/books")


@bp.route("search", methods=["GET"])
def search_books():
    """
    Search for books by title or author
    ---
    parameters:
      - name: title
        in: query
        type: string
        required: false
      - name: author
        in: query
        type: string
        required: false
    responses:
      200:
        description: A list of books and their availability
    """

    title = request.args.get("title", "", type=str)
    author = request.args.get("author", "", type=str)

    if not title and not author:
        return (
            jsonify(
                {
                    "error": "At least one of 'title' or 'author' query parameters must be provided."
                }
            ),
            400,
        )

    title = title.strip() if title else None
    author = author.strip() if author else None

    query = Book.query

    if title and author:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{title}%"),
                Book.authors.ilike(f"%{author}%"),
            )
        )
    elif title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    elif author:
        query = query.filter(Book.authors.ilike(f"%{author}%"))

    results = query.group_by(Book.book_id).all()

    books_list = []
    for book in results:
        is_wishlisted = db.session.query(
            db.session.query(Wishlist).filter(Wishlist.book_id == book.id).exists()
        ).scalar()

        books_list.append(
            {
                "id": book.id,
                "book_id": book.book_id,
                "isbn": book.isbn,
                "authors": book.authors,
                "publication_year": book.publication_year,
                "title": book.title,
                "language": book.language,
                "is_wishlisted": is_wishlisted,
            }
        )

    return jsonify(books_list)
