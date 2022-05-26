import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # # Method 1.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(int(request.form.get("sockets"))),
        has_toilet=bool(int(request.form.get("toilet"))),
        has_wifi=bool(int(request.form.get("wifi"))),
        can_take_calls=bool(int(request.form.get("calls"))),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the coffee price."})
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/random")
def get_cafe():
    random_cafe = random.choice(db.session.query(Cafe).all())
    cafe = random_cafe.__dict__
    cafe.pop('_sa_instance_state', None)
    return jsonify(cafe)


@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == 'sjsdbjie65d63hejbd':
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route("/all")
def get_all_cafe():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

    # cafes = db.session.query(Cafe).all()
    # random_cafe = random.choice(cafes)
    # return jsonify(cafe={
    #     # Omit the id from the response
    #     # "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #
    #     # Put some properties in a sub-category
    #     "amenities": {
    #         "seats": random_cafe.seats,
    #         "has_toilet": random_cafe.has_toilet,
    #         "has_wifi": random_cafe.has_wifi,
    #         "has_sockets": random_cafe.has_sockets,
    #         "can_take_calls": random_cafe.can_take_calls,
    #         "coffee_price": random_cafe.coffee_price,
    #     }
    # })

    # cafe_dict = OrderedDict()
    # cafes = db.session.query(Cafe).order_by(Cafe.id.desc()).all()
    # for index,cafe in enumerate(cafes):
    #     cafe =cafe.__dict__
    #     cafe.pop('_sa_instance_state', None)
    #     cafe_dict[index] = cafe
    #
    # print(cafe_dict)
    # return jsonify(cafe_dict)

    # cafe_list = []
    # cafes = db.session.query(Cafe).all()
    # for cafe in cafes:
    #     cafe = cafe.__dict__
    #     cafe.pop('_sa_instance_state', None)
    #     cafe_list.append(cafe)
    # cafe_dict = {'cafes':cafe_list}
    # print(cafe_dict)
    # return jsonify(cafe_dict)


# @app.route("/random")
# def get_cafe():
#     cafes = db.session.query(Cafe).all()
#     random_cafe = random.choice(cafes)
#     return jsonify(cafe={
#         "id": random_cafe.id,
#         "name": random_cafe.name,
#         "map_url": random_cafe.map_url,
#         "img_url": random_cafe.img_url,
#         "location": random_cafe.location,
#         "seats": random_cafe.seats,
#         "has_toilet": random_cafe.has_toilet,
#         "has_wifi": random_cafe.has_wifi,
#         "has_sockets": random_cafe.has_sockets,
#         "can_take_calls": random_cafe.can_take_calls,
#         "coffee_price": random_cafe.coffee_price,
#     })


@app.route('/search')
def search_cafes():
    location = request.args.get('loc')
    print(location)
    cafes = db.session.query(Cafe).filter(Cafe.location == location)
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/search_one")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
