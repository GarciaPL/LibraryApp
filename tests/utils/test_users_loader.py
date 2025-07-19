import textwrap

import pytest

from app import create_app, db
from app.db.models import User
from app.utils.users_loader import load_users


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


def test_load_users(tmp_path, init_database):
    csv_content = textwrap.dedent(
        """\
    User Name,User Type
    John,User
    Anna,Staff
    """
    )

    tmp_file = tmp_path / "books.csv"
    tmp_file.write_text(csv_content)

    load_users(str(tmp_file))

    users = User.query.all()
    assert len(users) == 2

    first_user = User.query.filter_by(user_name="John").first()
    assert first_user.user_name == "John"
    assert first_user.user_type == "User"

    second_user = User.query.filter_by(user_name="Anna").first()
    assert second_user.user_name == "Anna"
    assert second_user.user_type == "Staff"
