from datetime import datetime

from flask import jsonify, Blueprint

from app.db.models import Book, db, Rentals
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
