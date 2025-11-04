from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Camper, Activity, Signup
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"errors": ["validation errors"]}), 400

# Camper Routes
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers]), 200

@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify(camper.to_dict(include_signups=True)), 200

@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.get_json()
    
    try:
        camper = Camper(
            name=data.get('name'),
            age=data.get('age')
        )
        db.session.add(camper)
        db.session.commit()
        return jsonify(camper.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400  # FIXED: Generic error message

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        
        db.session.commit()
        return jsonify(camper.to_dict()), 202
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400  # FIXED: Generic error message

# Activity Routes
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    db.session.delete(activity)
    db.session.commit()
    return '', 204

# Signup Routes
@app.route('/signups', methods=['POST'])
def create_signup():
    data = request.get_json()
    
    try:
        signup = Signup(
            time=data.get('time'),
            camper_id=data.get('camper_id'),
            activity_id=data.get('activity_id')
        )
        db.session.add(signup)
        db.session.commit()
        
        # Return signup with nested camper & activity
        return jsonify(signup.to_dict(include_camper=True, include_activity=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400  # FIXED: Generic error message

# Home route (optional)
@app.route('/')
def home():
    return jsonify({
        "message": "Camping Fun API is running!",
        "available_endpoints": {
            "GET /campers": "List all campers",
            "GET /campers/<id>": "Get camper details with signups",
            "POST /campers": "Create a new camper",
            "PATCH /campers/<id>": "Update a camper",
            "GET /activities": "List all activities", 
            "DELETE /activities/<id>": "Delete an activity",
            "POST /signups": "Create a signup"
        }
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)