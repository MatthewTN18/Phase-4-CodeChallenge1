from flask import Flask
from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create campers
        campers = [
            Camper(name="Caitlin", age=8),
            Camper(name="Lizzie", age=9),
            Camper(name="Nicholas Martinez", age=12),
            Camper(name="Zoe", age=11)
        ]
        db.session.add_all(campers)
        db.session.commit()

        # Create activities
        activities = [
            Activity(name="Archery", difficulty=2),
            Activity(name="Swimming", difficulty=3),
            Activity(name="Hiking by the stream", difficulty=2),
            Activity(name="Listening to the birds chirp", difficulty=1)
        ]
        db.session.add_all(activities)
        db.session.commit()

        # Create signups
        signups = [
            Signup(camper_id=3, activity_id=3, time=8),
            Signup(camper_id=3, activity_id=4, time=1),
            Signup(camper_id=4, activity_id=2, time=9)
        ]
        db.session.add_all(signups)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()