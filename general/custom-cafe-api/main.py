from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "map_url": self.map_url,
            "img_url": self.img_url,
            "location": self.location,
            "seats": self.seats,
            "has_toilet": self.has_toilet,
            "has_wifi": self.has_wifi,
            "has_sockets": self.has_sockets,
            "can_take_calls": self.can_take_calls,
            "coffee_price": self.coffee_price
        }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_cafe():
    # Get the cafe list from the database
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()

    # Select a random one
    chosen_cafe = random.choice(all_cafes)

    # Serialization
    return jsonify(cafe=
                   {"name": chosen_cafe.name,
                    "map_url": chosen_cafe.map_url,
                    "img_url": chosen_cafe.img_url,
                    "location": chosen_cafe.location,
                    "amenities": {
                        "seats": chosen_cafe.seats,
                        "has_toilet": chosen_cafe.has_toilet,
                        "has_wifi": chosen_cafe.has_wifi,
                        "has_sockets": chosen_cafe.has_sockets,
                        "can_take_calls": chosen_cafe.can_take_calls,
                        "coffee_price": chosen_cafe.coffee_price,
                    }
                    }
                   )


@app.route("/all", methods=["GET"])
def get_all_cafes():
    # Get the cafe list from the database
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    list_to_add = [cafe.to_dict() for cafe in all_cafes]
    # Serialization
    return jsonify(cafes=list_to_add)


@app.route("/search", methods=["GET"])
def get_cafes_by_loc():
    # Flask does not automatically pass query parameters (like loc) as arguments to the route function.
    # Can't use sth like `def get_cafes_by_loc(loc)`
    # Flask expects positional arguments to come from the URL path.
    # To handle query parameters in a GET request, you need to extract them using Flask's request.args.
    loc = request.args.get('loc')

    # Check if the location exists in the database
    location_exists = db.session.execute(
        db.select(Cafe.location).distinct().where(Cafe.location == loc)
    ).first()

    if not location_exists:
        # If the location doesn't exist, return an error response
        return jsonify({"error":
                            {"Not Found": "Sorry, we don't have a cafe at that location."}
                        }), 404

    result = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
    result_by_loc = result.scalars().all()

    # Convert results to a list of dictionaries
    list_to_add_by_loc = [cafe.to_dict() for cafe in result_by_loc]

    return jsonify(cafes=list_to_add_by_loc)


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def get_new_cafe():
    new_cafe = Cafe(
        name=request.args.get('name'),
        map_url=request.args.get('map_url'),
        img_url=request.args.get('img_url'),
        location=request.args.get('location'),
        seats=request.args.get('seats'),
        has_toilet=bool(request.args.get('has_toilet')),  # Convert to boolean
        has_wifi=bool(request.args.get('has_wifi')),  # Convert to boolean
        has_sockets=bool(request.args.get('has_sockets')),  # Convert to boolean
        can_take_calls=bool(request.args.get('can_take_calls')),  # Convert to boolean
        coffee_price=request.args.get('coffee_price'),
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify({"response":
                        {"Success": "Successfully added the new cafe."}
                    }), 200


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_cafe(cafe_id):
    cafe_to_patch = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()

    if not cafe_to_patch:
        return jsonify({"response":
                            {"Error": f"Cafe with id {cafe_id} not found"}
                        }), 404

    new_cafe_price = request.args.get('new_price')
    cafe_to_patch.coffee_price = new_cafe_price
    db.session.commit()

    return jsonify({"response":
                        {"Success": "Successfully updated the price."}
                    }), 200


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()

    if not cafe_to_delete:
        return jsonify({"response":
                            {"Error": f"Cafe with id {cafe_id} not found"}
                        }), 404

    api_key = request.args.get('api-key')
    if api_key == "TopSecretAPIKey":
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify({"response":
                            {"Success": "Successfully removed the cafe."}
                        }), 200
    else:
        return jsonify({"response":
                            {"error": "Sorry, the operation is not allowed. Make sure your API key is correct."}
                        }), 403


if __name__ == '__main__':
    app.run(debug=True)
