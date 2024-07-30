# people.py
from flask import abort, make_response

from config import db
from models import Person, people_schema, person_schema


def read_all():
    people = Person.query.all()
    return people_schema.dump(people)


def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is None:
        abort(406, f"{lname} not found")
    return person_schema.dump(person)


def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person is None:
        abort(404, f"{lname} not found")

    update_person = person_schema.load(person, session=db._set_rel_query)
    existing_person.fname = update_person.fname
    db.session.merge(existing_person)
    db.session.commit()
    return person_schema.dump(existing_person), 201


def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person is None:
        abort(404, f"{lname} not found")

    db.session.delete(existing_person)
    db.session.commit()
    return make_response(f"{lname} successfully deleted", 200)


def create(person):
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person is not None:
        abort(406, f"{lname} already exists")
    new_person = person_schema.load(person, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return person_schema.dump(new_person), 201
