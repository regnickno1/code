from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Author {self.name}>'

class Catalogue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    books = db.relationship('Book', backref='catalogue', lazy=True)

    def __repr__(self):
        return f'<Catalogue {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, 
                         db.ForeignKey('author.id', name='fk_book_author'), 
                         nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    catalogue_id = db.Column(db.Integer, 
                           db.ForeignKey('catalogue.id', name='fk_book_catalogue'))

    def __repr__(self):
        return f'<Book {self.title}>'