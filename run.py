from app import create_app, db
from seed import main as seed_main

app = create_app()

with app.app_context():
    # Only seed if db is empty
    if not User.query.first():
        seed_main()        

if __name__ == "__main__":
    app.run()