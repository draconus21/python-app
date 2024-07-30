from pathlib import Path
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


basedir = Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

db_name = basedir / "people.db"
if not db_name.exists():
    print(f"creating db {db_name}")
    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect(str(db_name))
    columns = ", ".join(
        [
            "id INTEGER PRIMARY_KEY",
            "lname VARCHAR UNIQUE",
            "fname VARCHAR",
            "timestamp DATETIME",
        ]
    )
    create_table_cmd = f"CREATE TABLE person ({columns})"
    conn.execute(create_table_cmd)

    def get_timestamp():
        return str(datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

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
    insert_cmd_fmt = "INSERT INTO person VALUES ({})"
    for i, (_, person) in enumerate(PEOPLE.items()):
        data = ", ".join([str(i + 1), f'"{person["lname"]}"', f'"{person["fname"]}"', f'"{person["timestamp"]}"'])
        _cmd = insert_cmd_fmt.format(data)
        print(_cmd)
        print(" " * 16 + "^")
        conn.execute(_cmd)
    conn.commit()

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
