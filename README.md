FlaskRSSAtomParser
===

A Flask web application that parses feeds and other really cool magic.

Getting Started
===

Install virtualenv in your machine if you don't have one yet.

```
pip install virtualenv
```

Create virtualenv directory inside the project folder

```
virtualenv venv
```

Activate your virtual environment from the Scripts folder.

```
cd venv/Scripts
```

```
activate
```

Install the library and module requirements from the main directory

```
pip install -r requirements.txt
```

And now you should be good to go. To run the Flask server use the following command:

```
python manage.py runserver.

```
To run shell:

```
python manage.py shell
```


Built With
===

Python 3.6  
[Flask](http://flask.pocoo.org/docs/0.12/)
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
[Universal feedparser](https://pypi.python.org/pypi/feedparser)  
[Multiprocessing](https://docs.python.org/3/library/multiprocessing.html)


Author
===

Imran Abdallah
