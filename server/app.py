#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

from models import db, Dealership, Owner, Car

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

@app.get('/owners')
def get_owners():
    owners = Owner.query.all()
    return jsonify([owner.to_dict(rules=('-cars',)) for owner in owners]), 200

@app.get('/owners/<int:id>')
def get_owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()
    print(owner)
    return jsonify(owner.to_dict()), 201

@app.delete('/owners/<int:id>')
def delete_owner(id):
    owner = Owner.query.filter(Owner.id == id).first()
    db.session.delete(owner)
    db.session.commit()
    return jsonify(owner.to_dict()), 204

@app.get('/dealerships')
def get_dealerships():
    dealerships = Dealership.query.all()
    return jsonify([dealership.to_dict(rules=('-cars.owner','-cars.date_sold', '-cars.id')) for dealership in dealerships]), 200

@app.get('/dealerships/<int:id>')
def get_dealerships_by_id(id):
    try: 
        dealership = Dealership.query.filter(Dealership.id == id).first()
        return jsonify(dealership.to_dict()), 201
    except:
        return jsonify({"error": "dealership could not be found"}), 404

@app.post('/cars')
def create_car():
    data = request.json
    new_car = Car(
        make=data['make'],
        model=data['model'],
        owner_id=data['owner_id'],
        dealership_id=data['dealership_id'],
        date_sold=datetime.date(**data["date_sold"])
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify(new_car.to_dict()), 201

@app.delete('/cars/<int:id>')
def delete_car(id):
    try: 
        car = Car.query.filter(Car.id == id).first()
        db.session.delete(car)
        db.session.commit()
        return {}, 204
    except: 
        return jsonify({"error": "car could not be found"}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
