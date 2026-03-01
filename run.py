from app import create_app, db
from seed import main as seed_main

app = create_app()

with app.app_context():
    db.create_all()      # creates tables if missing
    seed_main()        

if __name__ == "__main__":
    app.run()