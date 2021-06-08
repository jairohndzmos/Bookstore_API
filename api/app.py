from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import dim_book_sf, dim_author_sf, dim_genre_sf, db, app


@app.route('/')
def main():
    return '<h3>Bookstore API</h3>'

@app.route('/add_book', methods=['POST'])
def post_book():

    query_parameters = request.json

    query = dim_book_sf(title=query_parameters["title"], author_id=query_parameters["author_id"], publisher_id=query_parameters["publisher_id"], genre_id=query_parameters["genre_id"], price=query_parameters["price"])

    db.session.add(query)

    db.session.commit() 

    return {"Response": "Book added!"}

@app.route('/delete_book', methods=['DELETE'])
def rid_book():

    query_parameters = request.args

    title = query_parameters.get("title").replace("+", " ") if query_parameters.get("title") else -1

    q = dim_book_sf.query.filter(dim_book_sf.title == title).one()

    db.session.delete(q)

    db.session.commit() 

    return {"Response": "Book deleted!"}



@app.route('/search_book', methods=['GET'])
def get_book():

    query_parameters = request.args

    title = query_parameters.get("title").replace("+", " ") if query_parameters.get("title") else -1
    author = query_parameters.get("author").replace("+", " ") if query_parameters.get("author") else -1 
    genre = query_parameters.get("genre").replace("+", " ") if query_parameters.get("genre") else -1

    query = (db.session.query(dim_book_sf.title, dim_author_sf.author, dim_genre_sf.genre)
        .join(dim_author_sf)
        .join(dim_genre_sf)
        .filter((dim_book_sf.title == title) | (dim_author_sf.author == author) | (dim_genre_sf.genre == genre))
        .order_by(dim_book_sf.title)
        ).all()

    results_dict = {}
    results_dict['results'] = []
    for book_title, author, genre in query:

        results_dict['results'].append({
            'title': book_title,
            'author': author,
            'genre': genre
        })

    return jsonify(results_dict)


if __name__ == "__main__":
    app.run(port=4040)
