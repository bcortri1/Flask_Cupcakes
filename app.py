from flask import Flask, redirect, render_template, jsonify , request
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension
import subprocess



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "I Love Cupcakes"



try:
    command = "psql -c 'create database cupcakes'"
    subprocess.call(command, shell = True)
except:
    print(Exception)


connect_db(app)

with app.app_context():
    db.create_all()

    
#===================================GET=======================================
@app.route("/", methods = ["GET"])
def frontend_cupcakes():
    """Diplays a JS & HTML template"""
    return render_template('index.html')


@app.route("/api/cupcakes", methods = ["GET"])
def get_all_cupcakes():
    """Gets data about all cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return ( jsonify(cupcakes=cupcakes), 200 )


@app.route("/api/cupcakes/<int:cupcake_id>",methods = ["GET"])
def get_cupcake(cupcake_id):
    """Gets data about one cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return ( jsonify(cupcake=cupcake.serialize()), 200 )


#===================================POST======================================
@app.route("/api/cupcakes",methods = ["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating
    and image data from the body of the request"""
    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"], 
        image=request.json["image"]
    )
    db.session.add(cupcake)
    db.session.commit()
    return ( jsonify(cupcake=cupcake.serialize()), 201 )


#==================================PATCH======================================
@app.route("/api/cupcakes/<int:cupcake_id>",methods = ["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL
    and flavor, size, rating and image data from the body of the request"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor=request.json.get("flavor",cupcake.flavor)
    cupcake.size=request.json.get("size",cupcake.size)
    cupcake.rating=request.json.get("rating",cupcake.rating)
    cupcake.image=request.json.get("image",cupcake.image)

    db.session.commit()
    return ( jsonify(cupcake=cupcake.serialize()), 200 )


#==================================DELETE=====================================
@app.route("/api/cupcakes/<int:cupcake_id>",methods = ["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes an existing cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return (jsonify(message="Deleted"), 200)