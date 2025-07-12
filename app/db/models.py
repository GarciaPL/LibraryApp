from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class Book(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    authors = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String)
    language = db.Column(db.String)

    wishlisted_by = db.relationship("Wishlist", back_populates="book")
    rental_items = db.relationship("Rentals", back_populates="book")

    def __repr__(self):
        return (
            f"<Book(id={self.id}, title='{self.title}', authors='{self.authors}', "
            f"isbn={self.isbn}, year={self.publication_year}, language='{self.language}')>"
        )


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False)

    wishlist = db.relationship("Wishlist", back_populates="user", uselist=False)
    rental_items = db.relationship("Rentals", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, user_name='{self.user_name}', user_type='{self.user_type}')>"


class Wishlist(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    user = db.relationship("User", back_populates="wishlist")
    book = db.relationship("Book", back_populates="wishlisted_by")

    def __repr__(self):
        return (
            f"<Wishlist(id={self.id}, user_id={self.user_id}, book_id={self.book_id})>"
        )


class Rentals(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = db.relationship("User", back_populates="rental_items")
    book = db.relationship("Book", back_populates="rental_items")

    def __repr__(self):
        return f"<Rentals(id={self.id}, user_id={self.user_id}, book_id={self.book_id} created_at={self.created_at})>"
