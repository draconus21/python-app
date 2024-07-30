# people.py
from flask import abort, make_response
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


PEOPLE = {
    "Fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "Ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "Bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    return list(PEOPLE.values())


def read_one(lname):
    if lname in PEOPLE:
        return PEOPLE[lname]

    abort(406, f"{lname} not found")


def update(lname, person):
    if lname not in PEOPLE:
        abort(404, f"{lname} not found")

    PEOPLE[lname]["fname"] = person.get("fname", PEOPLE[lname]["fname"])
    PEOPLE[lname]["timestamp"] = get_timestamp()
    return PEOPLE[lname]


def delete(lname):
    if lname not in PEOPLE:
        abort(404, f"{lname} not found")

    del PEOPLE[lname]
    return make_response(f"{lname} successfully deleted", 200)


def create(person):
    lname = person.get("lname")
    fname = person.get("lname", "")
    if lname and lname not in PEOPLE:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return PEOPLE[lname], 201

    abort(406, f"{lname} already exists")
