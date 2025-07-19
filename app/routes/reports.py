from datetime import datetime

from flask import jsonify, Blueprint
from sqlalchemy import func, desc

from app.db.models import Book, db, Rentals, User
from app.app_types.BookStatus import BookStatus

bp = Blueprint("reports", __name__, url_prefix="/v1/reports")


@bp.route("/amount/<string:status>", methods=["GET"])
def reports_amount_of_rented_books_with_delta(status):
    """
    Get report of books by rental status and days for how long they were rented for
    ---
    tags:
      - Reports
    parameters:
      - name: status
        in: path
        type: string
        required: true
        enum: [borrowed]
        description: Book status
    responses:
      200:
        description: Number of books with the given status and days for how long they were rented for
        schema:
          type: object
          properties:
            status:
              type: string
            count:
              type: integer
      400:
        description: Invalid status. Use 'borrowed'.
    """
    if not BookStatus.is_valid_status(status):
        return jsonify({"error": "Invalid status. Use 'borrowed'."}), 400

    records = (
        db.session.query(Book, Rentals).join(Rentals, Rentals.book_id == Book.id).all()
    )

    if records:
        now = datetime.now()
        results = [
            {
                "book_id": book.book_id,
                "title": book.title,
                "days_rented": get_delta(now, rentals.created_at),
            }
            for book, rentals in records
        ]
        return jsonify(results), 200

    return jsonify({"message": f"No books found with given status of {status}"}), 404


def get_delta(now: datetime, created_at: datetime) -> int:
    return (now - created_at).days


@bp.route("/top_rentals", methods=["GET"])
def reports_top_rentals():
    """
    Get a list of the top rented books.
    ---
    tags:
      - Reports
    summary: Top Rented Books Report
    description: Returns a list of books ordered by the number of rentals.
    responses:
      200:
        description: A list of top rented books
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                description: Title of the book
              authors:
                type: string
                description: Author(s) of the book
              rental_count:
                type: integer
                description: Number of times the book was rented
    """
    results = (
        db.session.query(
            Book.id,
            Book.title,
            Book.authors,
            func.count(Rentals.id).label("rental_count"),
        )
        .join(Rentals, Rentals.book_id == Book.id)
        .group_by(
            Book.id, Book.title, Book.authors
        )  # all not-aggregated columns from query
        .order_by(func.count(Rentals.id).desc())
        .all()
    )
    if results:
        report = [
            {"title": r.title, "authors": r.authors, "rental_count": r.rental_count}
            for r in results
        ]
        return jsonify(report)
    else:
        return jsonify({"error": "No rentals found"})


@bp.route("/top_rentals_by_username", methods=["GET"])
def reports_top_rentals_by_usernames():
    """
    Get a list of the top rented books with usernames
    ---
    tags:
      - Reports
    summary: Top Rented Books Report With Username
    description: Returns a list of books ordered by the number of rentals.
    responses:
      200:
        description: A list of top rented books by username
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                description: Title of the book
              user_name:
                type: string
                description: Username
              rental_count:
                type: integer
                description: Rental count
    """
    results = (
        db.session.query(
            Book.title, User.user_name, func.count(Rentals.id).label("rental_count")
        )
        .join(Rentals, Rentals.book_id == Book.id)
        .join(User, Rentals.user_id == User.id)
        .group_by(Book.title, User.user_name)  # all not-aggregated columns from query
        .order_by(desc("rental_count"))
        .all()
    )
    if results:
        report = [
            {"title": r.title, "user_name": r.user_name, "rental_count": r.rental_count}
            for r in results
        ]
        return jsonify(report)
    else:
        return jsonify({"error": "No rentals found"})
