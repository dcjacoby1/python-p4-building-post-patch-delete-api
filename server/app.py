#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

#GET request
#returns a list of games that pulls from the games table
@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = game.to_dict()
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

#returns a specific game
#game_dict turns the object from sql into a dictionary which is then converted into JSON
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )

        return response

    #POST creates a new Review instance based on the form data
    #adds it to DB with session add/commit
    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()

        response = make_response(
            review_dict,
            201
        )

        return response

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    #checks for matching ID in the DB
    review = Review.query.filter(Review.id == id).first()

    if review == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response
        #PATCH takes the review obj from line 95
        #loops through request.form dictionary and sets the object with the key:value pairs from the dictionary
        #set attribute takes 3 params: object we are updating, name of attr, value (dict) we are setting the value to
        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            db.session.add(review)
            db.session.commit()

            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response
        #DELETE takes the review object and deletes it
        elif request.method == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)