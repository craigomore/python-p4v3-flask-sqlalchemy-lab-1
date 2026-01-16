# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    quake = Earthquake.query.get(id)
    if quake:
        return make_response(quake.to_dict(), 200)
    else:
        return make_response({'message': f"Earthquake {id} not found."}, 404)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def quakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_list = [q.to_dict() for q in quakes]
    body = {
        'count': len(quakes_list),
        'quakes': quakes_list
    }
    return make_response(body, 200)


# Create tables and seed data if needed (helps tests run in this environment)
with app.app_context():
    db.create_all()

    # Seed only if earthquakes table is empty
    try:
        if Earthquake.query.count() == 0:
            db.session.add(Earthquake(magnitude=9.5, location="Chile", year=1960))
            db.session.add(Earthquake(magnitude=9.2, location="Alaska", year=1964))
            db.session.add(Earthquake(magnitude=8.6, location="Alaska", year=1946))
            db.session.add(Earthquake(magnitude=8.5, location="Banda Sea", year=1934))
            db.session.add(Earthquake(magnitude=8.4, location="Chile", year=1922))
            db.session.commit()
    except Exception:
        # If migrations are in use or table isn't present, ignore seeding here
        pass


if __name__ == '__main__':
    app.run(port=5555, debug=True)
