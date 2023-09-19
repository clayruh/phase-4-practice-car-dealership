#!/usr/bin/env python3

from app import app
from models import db, Dealership, Owner, Car
from faker import Faker
import random

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Deleting db...")
        Car.query.delete()
        Dealership.query.delete()
        Owner.query.delete()

        print("Seeding database...")
        owners_list = []
        for _ in range(5):
            owner = Owner(
                first_name=faker.first_name(),
                last_name=faker.last_name()
            )
            owners_list.append(owner)
            db.session.add_all(owners_list)
            db.session.commit()

        dealership_list = []
        for _ in range(5):
            dealership = Dealership(
                name = faker.company(),
                address = faker.street_address()
            )
            dealership_list.append(dealership)
            db.session.add_all(dealership_list)
            db.session.commit()

        cars_list = []
        manufacturers = ("Ford", "Chevrolet", "Toyota", "Chrysler", "Kia", "Tesla")

        for _ in range(10):
            car = Car(
                make=random.choice(manufacturers),
                model=faker.first_name(),
                date_sold=faker.date_between(start_date='-100y', end_date='today'),
                owner= random.choice(owners_list),
                dealership=random.choice(dealership_list)
            )
            cars_list.append(car)
            db.session.add_all(cars_list)
            db.session.commit()

        print("Seeding complete!")
