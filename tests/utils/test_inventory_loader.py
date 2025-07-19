import textwrap

import pytest

from app import create_app, db
from app.db.models import Book
from app.utils.inventory_loader import load_inventory


@pytest.fixture
def app():
    app = create_app(
        test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    with app.app_context():
        yield app


@pytest.fixture
def init_database(app):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


def test_load_inventory(tmp_path, init_database):
    csv_content = textwrap.dedent(
        """\
    Id,ISBN,Authors,Publication Year,Title,Language
    1,9780132350884,"Robert C. Martin",2008,Clean Code,en
    2,9780134685991,"Robert C. Martin",2017,Clean Architecture,en
    """
    )

    tmp_file = tmp_path / "inventory.csv"
    tmp_file.write_text(csv_content)

    load_inventory(str(tmp_file))

    books = Book.query.all()
    assert len(books) == 2

    first_book = Book.query.filter_by(isbn=9780132350884).first()
    assert first_book.authors == "Robert C. Martin"
    assert first_book.publication_year == 2008

    second_book = Book.query.filter_by(isbn=9780134685991).first()
    assert second_book.authors == "Robert C. Martin"
    assert second_book.publication_year == 2017
