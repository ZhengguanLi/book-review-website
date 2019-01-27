# Book Review Website
In this project, users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API. 

[Live Demo](https://bookstore-sugar.herokuapp.com/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisite

```
pip install -r requirements.txt
```

Set up the PostgreSQL hosted by Heroku, get the `DATABASE_URL`(more details: `project-book.pdf`)

Set `DATABASE_URL` in import.py and application.py

### Installation

Import books dataset from books.csv to database
```
python import.py
```

## Running the test

```
python application.py
```
And open the link on the terminal like below in your browser:
```
* Serving Flask app "application" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Deployment

Configure Procfile:
```
web: gunicorn application:app 
```

[Tutorial: Deploy app to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app)

## Author
* **Zhengguan Li**



