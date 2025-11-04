from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Camper(db.Model):
    __tablename__ = 'campers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    # Relationships
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    activities = association_proxy('signups', 'activity')
    
    # Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or age < 8 or age > 18:
            raise ValueError("Age must be an integer between 8 and 18")
        return age
    
    def to_dict(self, include_signups=False):
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
        if include_signups:
            data['signups'] = [signup.to_dict(include_activity=True) for signup in self.signups]
        return data

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    # Relationships
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    campers = association_proxy('signups', 'camper')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty
        }

class Signup(db.Model):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    
   
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    # Relationships
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    # Validations
    @validates('time')
    def validate_time(self, key, time):
        if not isinstance(time, int) or time < 0 or time > 23:
            raise ValueError("Time must be an integer between 0 and 23")
        return time
    
    @validates('camper_id')
    def validate_camper_id(self, key, camper_id):
        camper = Camper.query.get(camper_id)
        if not camper:
            raise ValueError("Camper not found")
        return camper_id
    
    @validates('activity_id')
    def validate_activity_id(self, key, activity_id):
        activity = Activity.query.get(activity_id)
        if not activity:
            raise ValueError("Activity not found")
        return activity_id
    
    def to_dict(self, include_camper=False, include_activity=False):
        data = {
            'id': self.id,
            'time': self.time,
            'camper_id': self.camper_id,
            'activity_id': self.activity_id
        }
        if include_camper:
            data['camper'] = self.camper.to_dict()
        if include_activity:
            data['activity'] = self.activity.to_dict()
        return data