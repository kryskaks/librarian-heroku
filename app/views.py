# -*- coding: utf-8 -*-
import random

from flask import request, render_template, redirect, url_for, session, flash
from functools import wraps
from app import app
from app.models import Book, Author, Authorship, db, User
from app.forms import SearchForm, AddEntityForm, UpdateAuthorForm, UpdateBookForm, LoginForm, RegistrationForm
from config import USERS
import constants

def auth_require_wrap(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		if not "user" in session:
			flash(constants.FLASH_MESSAGE_AUTH_REQUIRE)
			if request.method == "POST":
				return redirect(url_for('login'))
			return render_template("login.html", login_form = LoginForm(), referrer = url_for(func.__name__, **kwds))
			
			#flash(constants.FLASH_MESSAGE_AUTH_REQUIRE_BUTTON.format(login_url = url_for('login')))			
			#return redirect(request.referrer or url_for('index'))			
		
		return func(*args, **kwds)

	return wrapper

@app.route('/books')
def books_list():				
	return render_template('books.html', books = Book.query.all(), add_form = AddEntityForm())

@app.route('/books/create', methods = ["POST"])
@auth_require_wrap
def create_book():
	form = AddEntityForm(request.form)
	if not form.validate():
		return render_template('books.html', books = Book.query.all(), add_form = form)

	book = create(Book, form.text.data)
	return redirect(url_for('edit_book', id = book.id))

@app.route('/books/<int:id>')
def get_book(id):		
	book = Book.query.get(id)		
	if not book:
		return render_template('not_found.html'), 404
	return render_template('book.html', book = book)

@app.route('/books/<int:id>/edit')
@auth_require_wrap
def edit_book(id):	
	book = Book.query.get(id)	
	book_author_ids = [ath.author.id for ath in book.authorships]
	update_book_form = UpdateBookForm()	
	update_book_form.authors.choices = [(a.id, a.name) for a in Author.query.all() if a.id not in book_author_ids]

	return render_template('edit_book.html', book = book, update_book_form = update_book_form)

@app.route('/authors')
def authors_list():	
	return render_template('authors.html', authors = Author.query.all(), add_form = AddEntityForm())

@app.route('/authors/create', methods = ["POST"])
@auth_require_wrap
def create_author():	
	form = AddEntityForm(request.form)
	
	if not form.validate():
		return render_template('authors.html', authors = Author.query.all(), add_form = form)
	
	author = create(Author, form.text.data)
	flash(constants.FLASH_MESSAGE_AUTHOR_CREATED.format(name = author.name))		
	return redirect(url_for('authors_list'))

@app.route('/authors/<int:id>')
def get_author(id):		
	author = Author.query.get(id)		
	if not author:
		return render_template('not_found.html'), 404
	return render_template('author.html', author = author)

@app.route('/authors/<int:id>/edit')
@auth_require_wrap
def edit_author(id):		
	return render_template('edit_author.html', author = Author.query.get(id), update_form = UpdateAuthorForm())

@app.route('/authors/<int:id>/update', methods = ["POST"])
@auth_require_wrap
def update_author(id):	
	form = UpdateAuthorForm(request.form)
	author = Author.query.get(id)
	if not form.validate():
		return render_template('edit_author.html', author = author, update_form = form)
	
	author.name = form.text.data
	db.session.merge(author)
	db.session.commit()	
	return redirect(url_for('get_author', id = id))

def create(class_name, value):	
	o = class_name(value)
	db.session.add(o)
	db.session.commit()
	return o

@app.route('/authorship/<int:id>/delete')
@auth_require_wrap
def delete_authorship(id):
	authorship = Authorship.query.get(id)	
	name = authorship.author.name
	book_id = authorship.book.id
	db.session.delete(authorship)
	db.session.commit()
	flash(constants.FLASH_MESSAGE_BOOK_AUTHOR_DELETED.format(name = name))
	return redirect(url_for('edit_book', id = book_id))

@app.route('/books/<int:id>/delete')
@auth_require_wrap
def delete_book(id):
	book = Book.query.get(id)
	for authorship in book.authorships:
		db.session.delete(authorship)		
	db.session.delete(book)	
	db.session.commit()

	flash(constants.FLASH_MESSAGE_BOOK_DELETED.format(title = book.title))
	return redirect(url_for('books_list'))

@app.route('/')
def index():	
	db_books = Book.query.all()	
	books = set([db_books[i] for i in [random.randint(0, len(db_books) - 1) for j in xrange(5)]])
	return render_template('index.html', books = books, search_form = SearchForm())

@app.route('/search', methods = ["POST"])
def search():		
	search_form = SearchForm(request.form)
	if not search_form.validate():
		return render_template('search_result.html', books = [], search_form = search_form)

	search_phrase = "%%%s%%" % search_form.text.data

	books_by_title = Book.query.filter(Book.title.ilike(search_phrase)).all() if search_form.by_title.data else []
	authors_by_name = Author.query.filter(Author.name.ilike(search_phrase)).all() if search_form.by_author.data else []

	books = set(books_by_title + [authorship.book for author in authors_by_name for authorship in author.authorships])
	
	#form = SearchForm().set_defaults()
	form = SearchForm()	
	return render_template('search_result.html', books = books, search_form = form)


@app.route('/books/<int:id>/save', methods = ["POST"])
@auth_require_wrap
def save_book(id):	
	book = Book.query.get(id)
	form =  UpdateBookForm(request.form)	
	if not form.validate():
		book_author_ids = [ath.author.id for ath in book.authorships]
		form.authors.choices = [(a.name, a.name) for a in Author.query.all() if a.id not in book_author_ids]
		return render_template('edit_book.html', book = book, update_book_form = form)

	book.title = form.text.data
	
	authors = [Author.query.get(author_id) for author_id in form.authors.data]
	
	for author in authors:
		authorship = Authorship(book_id = id, author_id = author.id)
		db.session.add(authorship)
	
	db.session.merge(book)
	db.session.commit()

	return redirect(url_for('get_book', id = id))


@app.route('/authors/delete/<int:id>')
@auth_require_wrap
def delete_author(id):
	author = Author.query.get(id)
	for authorship in author.authorships:
		db.session.delete(authorship)		
	db.session.delete(author)
	
	db.session.commit()

	flash(constants.FLASH_MESSAGE_AUTHOR_DELETED.format(name = author.name))
	return redirect(url_for('authors_list'))

@app.route('/login', methods = ["POST", "GET"])
def login():	
	if request.method == "GET":
		return render_template("login.html", login_form = LoginForm(), referrer = request.referrer or url_for("index"))

	form = LoginForm(request.form)
	if not form.validate():
		return render_template("login.html", login_form = form, referrer = request.form["referrer"] or url_for("index"))

	session["user"] = form.login.data
		
	return redirect(request.form["referrer"] or url_for("index"))

@app.route('/logout')
def logout():
	session.pop("user", None)	
	return redirect(request.referrer or url_for("index"))

@app.errorhandler(500)
def error(e):
    return render_template('error.html'), 500

@app.errorhandler(404)
def error(e):
    return render_template('not_found.html'), 404

@app.route('/register', methods = ["POST", "GET"])
def register():
	if request.method == "GET":
		return render_template("register.html", registration_form = RegistrationForm(), referrer = request.referrer or url_for('index'))

	form = RegistrationForm(request.form)	
	if not form.validate():
		return render_template("register.html", registration_form = form, referrer = request.form["referrer"] or url_for('index'))

	user = User.query.filter_by(login = form.login.data).all()

	if user:
		form.login.errors.append(constants.ERROR_USER_ALREADY_REGISTERED.format(name = form.login.data))
		return render_template("register.html", registration_form = form, referrer = request.form["referrer"] or url_for('index'))

	user = User(login = form.login.data, password = form.password.data)
	db.session.add(user)
	db.session.commit()
	
	session["user"] = user.login

	flash(constants.FLASH_MESSAGE_USER_REGISTERED.format(name = form.login.data))	
	return redirect(request.form["referrer"] or url_for("index"))