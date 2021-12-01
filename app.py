"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "p-word-here-shhhhh"

connect_db(app)

@app.route("/")
def root():
    """Homepage"""

    return render_template("home.html")

@app.route("/api/cupcakes")
def all_cupcake_data():

    cupcake = Cupcake.query.all()
    cupcakes = [c.serialize_cupcakes() for c in cupcake]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_a_cupcake():
    """Creat a new cupcake and post it"""
    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        size= data['size'],
        rating = data['rating'],
        image = data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize_cupcakes()), 201)



@app.route("/api/cupcakes/<int:c_id>")
def get_cupcake_data(c_id):
    """get a specific cupcakes data and info"""
    
    cupcake = Cupcake.query.get_or_404(c_id)
    return jsonify(cupcake=cupcake.serialize_cupcakes())

@app.route("/api/cupcakes/<int:c_id>", methods=["PATCH"])
def update_cupcake_data(c_id):
    """update cupcake data and return the updated cupcake data"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(c_id)
    cupcake.flavor = data['flavor']
    cupcake.size= data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize_cupcakes())

@app.route("/api/cupcakes/<int:c_id>", methods=["DELETE"])
def delete_cupcake_data(c_id):
    """delete cupcake and return a message indicating the deletion was processed"""

    cupcake = Cupcake.query.get_or_404(c_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")


    
