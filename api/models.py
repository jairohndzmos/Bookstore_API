from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookstore.db"
app.config['DEBUG'] = True
db = SQLAlchemy(app)

class dim_genre_sf(db.Model):
    __tablename__ = "dim_genre_sf"
    id = db.Column("genre_id", db.Integer, primary_key=True)
    genres = db.relationship("dim_book_sf", passive_deletes=True, backref=db.backref('genre_ref',lazy='joined'), lazy='select') #ONE
    genre = db.Column(db.String(128), nullable=False)

class dim_publisher_sf(db.Model):
    __tablename__ = "dim_publisher_sf"
    id = db.Column("publisher_id", db.Integer, primary_key=True)
    authors = db.relationship("dim_book_sf", passive_deletes=True, backref=db.backref('publisher_ref',lazy='joined'), lazy='select') #ONE
    publisher = db.Column(db.String(256), nullable=False)

class dim_author_sf(db.Model):
    __tablename__ = "dim_author_sf"
    id = db.Column("author_id", db.Integer, primary_key=True)
    authors = db.relationship("dim_book_sf", passive_deletes=True, backref=db.backref('authors_ref',lazy='joined'), lazy='select') #ONE
    author = db.Column(db.String(256), nullable=False)

class dim_book_sf(db.Model):
    __tablename__ = "dim_book_sf"
    id = db.Column("book_id", db.Integer, primary_key=True) 
    books = db.relationship("fact_booksales", passive_deletes=True, backref=db.backref('book',lazy='joined'), lazy='select')
    title = db.Column(db.String(256), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("dim_author_sf.author_id", ondelete='CASCADE'), nullable=False) #MANY
    publisher_id = db.Column(db.Integer, db.ForeignKey("dim_publisher_sf.publisher_id", ondelete='CASCADE'), nullable=False) #MANY
    genre_id = db.Column(db.Integer, db.ForeignKey("dim_genre_sf.genre_id", ondelete='CASCADE'), nullable=False) #MANY
    price = db.Column(db.Float, nullable=False)

#ONE

class dim_store_sf(db.Model):
    __tablename__ = "dim_store_sf"
    id = db.Column("store_id", db.Integer, primary_key=True) 
    stores = db.relationship("fact_booksales", passive_deletes=True, backref=db.backref('store_ref',lazy='joined'), lazy='select')
    store_address = db.Column(db.String(256), nullable=False)

#ONE

class fact_booksales(db.Model):
    __tablename__ = "fact_booksales"
    id = db.Column("sales_id", db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("dim_book_sf.book_id", ondelete='CASCADE'), nullable=False) 
    store_id = db.Column(db.Integer, db.ForeignKey("dim_store_sf.store_id", ondelete='CASCADE'), nullable=False) 
    quantity = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
#MANY