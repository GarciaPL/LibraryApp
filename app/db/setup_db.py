from app import create_app
import os

INVENTORY_USERS = "data\\users.csv"
INVENTORY_DATA = "data\\book_inventory.csv"

app = create_app()
basedir = os.path.abspath(os.path.dirname(__file__))


def load_bootstrap_data():
    with app.app_context():
        from app.utils.inventory_loader import load_inventory
        from app.utils.users_loader import load_users

        base_dir = os.path.abspath(os.path.dirname(__file__))
        book_inventory_path = os.path.join(base_dir, INVENTORY_DATA)
        users_path = os.path.join(base_dir, INVENTORY_USERS)
        load_inventory(book_inventory_path)
        load_users(users_path)
