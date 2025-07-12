from datetime import datetime

from flask import Blueprint
from flask import jsonify

from app.db.models import Book, db, Wishlist, Rentals
from app.app_types.BookStatus import BookStatus

from app.notifications import notifications

bp = Blueprint("rentals", __name__, url_prefix="/v1/rentals")


@bp.route("/<int:book_id>", methods=["POST"])
def change_rental_status(book_id):
    """
    Change the rental status of a book
    ---
    tags:
      - Rentals
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book to change status for
    responses:
      200:
        description: Status changed successfully
        examples:
          application/json:
            message: "Status of the book 'Book Title' has been changed from borrowed to available"
      404:
        description: Book not found / No rentals found
        examples:
          application/json:
            error: "Book not found / No rentals found"
    """

    book = get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    rental_of_book = get_rental(book)
    if rental_of_book:
        # if rental exists in database, we assume that book is borrowed, so we will make it available
        # we will fetch rentals with books and then remove the rental and notify users who had this book on a wishlist
        rentals_with_book = get_rentals_with_book(book)

        db.session.delete(rental_of_book)
        db.session.commit()

        for wishlist_for_book in get_wishlists(book):
            notifications.notify(
                user_name=wishlist_for_book.user.user_name, book_title=book.title
            )

        if rentals_with_book:
            results = [
                {
                    "book_id": book.id,
                    "book_title": book.title,
                    "book_status": BookStatus.AVAILABLE.value,
                }
                for rentals, book in rentals_with_book
            ]
            return jsonify(results), 200
        else:
            return jsonify({"message": f"No rentals found"}), 404
    else:
        # if rental does not exist in database, we assume that book it's ready to be borrowed
        # fetch first wishlist among all users and create a rental for that user
        # remove wishlist for given user
        # notify only user who is going to be eligible to borrow a book
        wishlists_for_book = get_wishlists(book)
        if wishlists_for_book:
            first_wishlist = wishlists_for_book[0]
            first_user_with_wishlist_for_book = first_wishlist.user

            new_rental = Rentals(
                user_id=first_user_with_wishlist_for_book.id,
                book_id=book.id,
                created_at=datetime.now(),
            )

            db.session.add(new_rental)
            db.session.delete(first_wishlist)
            db.session.commit()

            notifications.notify(
                user_name=first_user_with_wishlist_for_book.user_name,
                book_title=book.title,
            )

            rentals_with_book = get_rentals_with_book(book)

            if rentals_with_book:
                results = [
                    {
                        "book_id": book.id,
                        "book_title": book.title,
                        "book_status": BookStatus.BORROWED.value,
                    }
                    for rentals, book in rentals_with_book
                ]
                return jsonify(results), 200
            else:
                return jsonify({"message": f"No rentals found"}), 404
        else:
            return (
                jsonify(
                    {"message": f"No wishlists found being linked to {book.title}"}
                ),
                404,
            )


def get_book(book_id: int) -> Book | None:
    return Book.query.filter_by(book_id=book_id).first()


def get_rental(book: Book) -> Rentals | None:
    return Rentals.query.filter_by(book_id=book.id).first()


def get_rentals_with_book(book: Book) -> list[tuple[Rentals, Book]]:
    return (
        db.session.query(Rentals, Book)
        .join(Book, Rentals.book_id == Book.id)
        .filter(Book.id == book.id)
        .all()
    )


def get_wishlists(book: Book) -> list[Wishlist]:
    return Wishlist.query.filter_by(book_id=book.id).all()
