# Project 1

Web Programming with Python and JavaScript

To run the project on your local machine or build it by your self, 
please follow the steps bellow:

* Clone this repository,
* Run `pip install` to install all dependencies from `requirements.text`,
* Run `npm install` to install front-end build dependencies,
then run `npm run prod` to build assets.

Create a `.env` file to the root directory or run `export VARIABLE_NAME=VALUE`  to store the environment variables.
The following variables are required: `DATABASE_URL`, `API_KEY`, and `SECRET_KEY`.

Signup to [https://www.goodreads.com/api](https://www.goodreads.com/api) for Goodreada account
and follow the step to get the API_KEY.

The migration file and seed file are found in `database_migrations` directory,
and `import.py` file in the root directory. So, run `python database_migrations/create_tables`
to create tables in th database and then run `python import.py` to populate the books table and `python import_rating.py`
to populate the `average_ratings` table.

Run `ptyhon run.py` to start the server.  

## Demo

[http://book-review.kkanangila.com/](http://book-review.kkanangila.com/)

Note: The application is hosted on heroku free dynos, It can take time to load if the server is in standby. 
