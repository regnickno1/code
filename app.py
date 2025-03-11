from flask import Flask, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate
from models import db, Book, Author, Catalogue
from forms import BookForm, AuthorForm, CatalogueForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Create tables within app context
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Author routes
@app.route('/authors')
def list_authors():
    authors = Author.query.all()
    return render_template('authors/list.html', authors=authors)

@app.route('/authors/new', methods=['GET', 'POST'])
def create_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(
            name=form.name.data,
            date_of_birth=form.date_of_birth.data
        )
        db.session.add(author)
        db.session.commit()
        flash('Author created successfully!', 'success')
        return redirect(url_for('list_authors'))
    return render_template('authors/form.html', form=form, title="Create Author")

@app.route('/authors/<int:id>/edit', methods=['GET', 'POST'])
def edit_author(id):
    author = Author.query.get_or_404(id)
    form = AuthorForm(obj=author)
    if form.validate_on_submit():
        author.name = form.name.data
        author.date_of_birth = form.date_of_birth.data
        db.session.commit()
        flash('Author updated successfully!', 'success')
        return redirect(url_for('list_authors'))
    return render_template('authors/form.html', form=form, title="Edit Author")

@app.route('/authors/<int:id>/delete', methods=['POST'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully!', 'warning')
    return redirect(url_for('list_authors'))

# Book routes
@app.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('books/list.html', books=books)

@app.route('/books/new', methods=['GET', 'POST'])
def create_book():
    form = BookForm()
    form.author_id.choices = [(a.id, a.name) for a in Author.query.all()]
    form.catalogue_id.choices = [(0, '-- Select Catalogue --')] + [(c.id, c.name) for c in Catalogue.query.order_by('name').all()]
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author_id=form.author_id.data,
            catalogue_id=form.catalogue_id.data,
            year_published=form.year_published.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book created successfully!', 'success')
        return redirect(url_for('list_books'))
    return render_template('books/form.html', form=form, title="Create Book")

@app.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    form.author_id.choices = [(a.id, a.name) for a in Author.query.all()]
    form.catalogue_id.choices = [(0, '-- Select Catalogue --')] + [(c.id, c.name) for c in Catalogue.query.order_by('name').all()]
    if form.validate_on_submit():
        book.title = form.title.data
        book.author_id = form.author_id.data
        book.catalogue_id = form.catalogue_id.data
        book.year_published = form.year_published.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('list_books'))
    return render_template('books/form.html', form=form, title="Edit Book")

@app.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'warning')
    return redirect(url_for('list_books'))

# Catalogue routes
@app.route('/catalogues')
def list_catalogues():
    catalogues = Catalogue.query.all()
    return render_template('catalogue/list.html', catalogues=catalogues)

@app.route('/catalogues/create', methods=['GET', 'POST'])
def create_catalogue():
    form = CatalogueForm()
    if form.validate_on_submit():
        catalogue = Catalogue(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(catalogue)
        db.session.commit()
        flash('Catalogue created successfully!', 'success')
        return redirect(url_for('list_catalogues'))
    return render_template('catalogue/form.html', form=form, title='Create Catalogue')

@app.route('/catalogues/<int:id>/edit', methods=['GET', 'POST'])
def edit_catalogue(id):
    catalogue = Catalogue.query.get_or_404(id)
    form = CatalogueForm(obj=catalogue)
    if form.validate_on_submit():
        catalogue.name = form.name.data
        catalogue.description = form.description.data
        db.session.commit()
        flash('Catalogue updated successfully!', 'success')
        return redirect(url_for('list_catalogues'))
    return render_template('catalogue/form.html', form=form, title='Edit Catalogue')

@app.route('/catalogues/<int:id>/delete', methods=['POST'])
def delete_catalogue(id):
    catalogue = Catalogue.query.get_or_404(id)
    db.session.delete(catalogue)
    db.session.commit()
    flash('Catalogue deleted successfully!', 'success')
    return redirect(url_for('list_catalogues'))

if __name__ == '__main__':
    app.run(debug=True)