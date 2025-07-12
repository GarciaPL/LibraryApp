from app import create_app, db
from app.db.setup_db import load_bootstrap_data

app = create_app()

print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.methods} -> {rule.rule}")

if __name__ == "__main__":
    print("Create tables")
    with app.app_context():
        db.create_all()
    print("Tables created!")

    print("Load bootstrap data")
    load_bootstrap_data()
    print("Bootstrap data loaded!")

    app.run(debug=True)
