from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    cars = db.relationship('Car', back_populates='owner')
    dealership = association_proxy('cars', 'dealership')
    serialize_rules = ('-cars.owner',)

    def __repr__(self):
        return f"<Owner {self.id}: first_name={self.first_name}, last_name={self.last_name}>"
    
class Dealership(db.Model, SerializerMixin):
    __tablename__ = 'dealerships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    cars = db.relationship('Car', back_populates='dealership')
    owner = association_proxy('cars', 'owner')
    serialize_rules = ('-cars.dealership',)

class Car(db.Model, SerializerMixin):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    date_sold = db.Column(db.Date, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    dealership_id = db.Column(db.Integer, db.ForeignKey('dealerships.id'))

    owner = db.relationship("Owner", back_populates="cars")
    dealership = db.relationship("Dealership", back_populates='cars')
    serialize_rules = ('-owner.cars', '-dealership.cars', '-dealership_id', '-owner_id')

    @validates('make')
    def validate_make(self, key, value):
        manufacturers = ("Ford", "Chevrolet", "Toyota", "Chrysler", "Kia", "Tesla")
        # if value is inside manufacturers, return value
        if value in manufacturers:
            return value
        return ValueError("manufacturer not in list")