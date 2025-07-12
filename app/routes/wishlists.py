from flask import jsonify, Blueprint

from app.db.models import User, Book, Wishlist, db
from app.notifications import notifications

bp = Blueprint("wishlists", __name__, url_prefix="/v1/wishlists")


@bp.route("/<string:user_name>/<int:book_id>", methods=["POST"])
def add_to_wishlist(user_name, book_id):
    """
    ---
    summary: Add a book to a user's wishlist
    parameters:
      - in: path
        name: user_name
        schema:
          type: string
        required: true
        description: Username of the user adding to wishlist
      - in: path
        name: book_id
        schema:
          type: integer
        required: true
        description: ID of the book to add
    responses:
      201:
        description: Book successfully added to wishlist
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      200:
        description: Book already in wishlist
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: User or book not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    security:
      - ApiKeyAuth: []
    """

    user = get_user(user_name)
    if not user:
        return jsonify({"error": "User not found"}), 404

    book = get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    existing_wishlist_given_user = Wishlist.query.filter_by(
        user_id=user.id, book_id=book.id
    ).first()
    if existing_wishlist_given_user and existing_wishlist_given_user.user_id == user.id:
        return (
            jsonify(
                {
                    "message": f"Given user '{user_name}' already has this book in a wishlist"
                }
            ),
            200,
        )

    existing_wishlist_other_user = Wishlist.query.filter_by(book_id=book.id).first()
    if existing_wishlist_other_user:
        return jsonify({"message": "Book already in wishlist of other user"}), 200

    wishlist_entry = Wishlist(user=user, book=book)
    db.session.add(wishlist_entry)
    db.session.commit()

    notifications.notify(user_name=user.user_name, book_title=book.title)

    return (
        jsonify(
            {
                "message": f"Book '{book.title}' added to user {user.user_name}'s wishlist"
            }
        ),
        201,
    )


@bp.route("/<string:user_name>/<int:book_id>", methods=["DELETE"])
def remove_from_wishlist(user_name, book_id):
    """
    ---
    summary: Remove a book from a user's wishlist
    parameters:
      - in: path
        name: user_name
        schema:
          type: string
        required: true
        description: Username of the user
      - in: path
        name: book_id
        schema:
          type: integer
        required: true
        description: ID of the book to remove
    responses:
      204:
        description: Book successfully removed from wishlist (No Content)
      404:
        description: User or book not found, or book not in wishlist
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    security:
      - ApiKeyAuth: []
    """

    user = get_user(user_name)
    if not user:
        return jsonify({"error": "User not found"}), 404

    book = get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    existing_wishlist_given_user = Wishlist.query.filter_by(
        user_id=user.id, book_id=book.id
    ).first()

    if not existing_wishlist_given_user:
        return (
            jsonify(
                {
                    "message": f"Given user '{user_name}' does not have book {book.title} in a wishlist"
                }
            ),
            404,
        )

    db.session.delete(existing_wishlist_given_user)
    db.session.commit()

    notifications.notify(user_name=user.user_name, book_title=book.title)

    return (
        jsonify(
            {
                "message": f"Book '{book.title}' has been removed from {user.user_name}'s wishlist"
            }
        ),
        204,
    )


def get_book(book_id: int) -> Book:
    return Book.query.filter_by(book_id=book_id).first()


def get_user(user_name: str) -> User:
    return User.query.filter_by(user_name=user_name).first()
