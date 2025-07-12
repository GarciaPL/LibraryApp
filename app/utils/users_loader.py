import pandas as pd
from app import db, create_app
from app.db.models import User

app = create_app()


def load_users(csv_path):
    df = pd.read_csv(csv_path, header=0, skip_blank_lines=True)

    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()

        users = []
        for _, row in df.iterrows():
            print(f"Row {row=}")
            user = User(user_name=row["User Name"], user_type=row["User Type"])
            users.append(user)

        db.session.add_all(users)
        db.session.commit()
        print(f"Inserted {len(df)} user into the database.")
