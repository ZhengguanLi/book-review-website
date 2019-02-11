# Book Review Website

In this project, users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

[Live Demo](https://bookstore-sugar.herokuapp.com/)

## Getting Started

### Requirements

- Python >= 3.7

### Prerequisite

- Install prerequisite packages

    ```shell
    pip install -r requirements.txt
    ```

- Set up the PostgreSQL hosted by **Heroku**, get the `DATABASE_URL`

- Set `DATABASE_URL` in import.py and application.py

    ```python
        10  DATABASE_URL=''
    ```

### Installation

- Import books dataset from **books.csv** to database

    ```shell
    python import.py
    ```

## Running the test

- Execute

    ```shell
    python application.py
    ```

- Open the link on the terminal like below in your browser

    ```shell
    * Serving Flask app "application" (lazy loading)
    * Environment: production
    WARNING: Do not use the development server in a production environment.
    Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

## Deployment

- Configure **Procfile**

    ```text
    web: gunicorn application:app
    ```

- [Tutorial: Deploy app to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app)

## Contribution

- [Goodreads](https://www.goodreads.com/) - A "social cataloging" website to freely search database of books, annotations, and reviews.
- [Heroku](https://www.heroku.com/) - A cloud platform as a service.

## Author

- Zhengguan