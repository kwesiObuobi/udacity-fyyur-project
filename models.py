

from datetime import datetime
from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. -- (completed by Samuel Lartey)
shows_table = db.Table('Show', 
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
  db.Column('start_date', db.DateTime, default=datetime.now()),
  db.Column('image_link', db.String)
)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate -- (completed by Samuel Lartey)
    genres = db.Column(db.String)
    website_link = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String())
    artists = db.relationship('Artist', secondary=shows_table, backref=db.backref('venues', lazy=True))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate -- (completed by Samuel Lartey)
    genres = db.Column(db.String)
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String())
