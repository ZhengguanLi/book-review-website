import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# configuration
DATABASE_URL=''

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True # pretty
app.config['DEBUG'] = 1 # debug mode on
Session(app)

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/accounts/login")
def login_page(msg=''):
    title = "Sign In - Book Reviews"
    submit_btn_text = "Sign In"
    return render_template("./accounts/login.html", title = title, submit_btn_text = submit_btn_text, msg = msg)

@app.route("/accounts/signup")
def signup_page(msg=''):
    title = "Sign Up - Book Reviews"
    submit_btn_text = "Sign Up"
    return render_template("./accounts/signup.html", title = title, submit_btn_text = submit_btn_text, msg = msg)

@app.route("/accounts/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/accounts/signup/status", methods=["post"])
def signup():
    email_address = request.form.get("email_address")
    username = request.form.get("username")
    password = request.form.get("password")
    if db.execute("Select * from accounts where email_address = :email_address", {"email_address": email_address}).rowcount == 0:
        db.execute("INSERT INTO accounts(email_address, username, password) VALUES (:email_address, :username, :password)", {"email_address": email_address, "username": username, "password": password})
        db.commit()
        return signup("Account created successfully, please log in!")
    else:
        return signup("The email address has been bound to another user, try another email address!")   

@app.route("/accounts/login/status", methods=["post"])
def login():
    email_address = request.form.get("email_address")
    password = request.form.get("password")
    account_info = db.execute("SELECT * from accounts where email_address = :email_address AND password = :password", {"email_address": email_address, "password": password}).fetchall()
    if account_info:
        for info in account_info:
            session['email_address'] = info['email_address']
            session['username'] = info['username']
        return search_page()
    else:
        return login("Email/Password unmatched!")

@app.route("/search")
def search_page():
    return render_template("search.html", result=None)

@app.route("/search/result", methods=['post'])
def search():
    search_value = request.form.get('search_input')
    result = db.execute("SELECT * from books where isbn = :isbn", {'isbn':search_value}).fetchall()
    if len(result) != 0:
        return render_template('search.html', result = result)
    result = db.execute("SELECT * from books where title = :title", {'title':search_value}).fetchall()
    if len(result) != 0:
        return render_template('search.html', result = result)
    result = db.execute("SELECT * from books where author = :author", {'author':search_value}).fetchall()
    if len(result) != 0:
        return render_template('./search.html', result = result)
    return render_template('search.html', result = result)

@app.route("/search/bookreview/<isbn>")
def book_review_page(isbn='', err_msg=''):
    # add review from the goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Of50BiovbVKuGis0N8109g", "isbns": "074349671X"})
    goodreads_review = ''
    if res.status_code != 200:
        raise Exception("Error: API request is unsuccessful.")
    else:
        goodreads_review = res.json()

    # add review from the database
    book_basic_info = db.execute("SELECT * from books where isbn=:isbn", {'isbn':isbn}).fetchone()
    book_avg_rating = db.execute("SELECT avg(rating) from reviews where isbn=:isbn", {'isbn':isbn}).scalar()
    book_avg_rating = 0 if book_avg_rating is None else book_avg_rating
    book_reviews = db.execute("SELECT * from reviews where isbn=:isbn", {'isbn':isbn}).fetchall()
    return render_template('bookreview.html', book_basic_info = book_basic_info, book_avg_rating = book_avg_rating, book_reviews = book_reviews, goodreads_review = goodreads_review, err_msg = err_msg)

@app.route("/search/book/addreview/<isbn>", methods=['post'])
def add_review(isbn):
    review = request.form.get('review')
    rating = request.form.get('radAnswer')
    is_exist = db.execute("SELECT count(*) from reviews where email_address=:email_address and isbn=:isbn", {'email_address':session['email_address'], 'isbn':isbn}).scalar()
    if is_exist == 1:
        err_msg = "You have already added the review for this book."
        return book_review_page(isbn, err_msg)
    else:
        db.execute("INSERT INTO reviews(email_address, isbn, review, rating) VALUES (:email_address, :isbn, :review, :rating)", { 'email_address':session['email_address'], 'isbn':isbn, 'review':review, 'rating':rating})
        db.commit()
        return book_review_page(isbn)

@app.route("/api/<isbn>", methods=["get"])
def api_access(isbn):
    res1 = db.execute("SELECT * from books where isbn=:isbn", {"isbn": isbn}).fetchone()
    if res1 is None:
        #return jsonify({"err": "Invalid ISBN"}), 404
        return render_template("404.html"), 404

    res = dict(res1)
    res2 = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Of50BiovbVKuGis0N8109g", "isbns": isbn})
    goodreads_review = ''
    if res2.status_code != 200:
        raise Exception("Error: API request is unsuccessful.")
    else:
        goodreads_review = res2.json()
    res['review_count'] = goodreads_review['books'][0]['work_reviews_count']
    res['average_score'] = goodreads_review['books'][0]['average_rating']
    return jsonify( isbn=res['isbn'],
                    title=res['title'],
                    author=res['author'],
                    year=res['year'],
                    review_count=res['review_count'],
                    average_score=res['average_score'])

if __name__ == '__main__':
	app.run()