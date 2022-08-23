#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import babel
import dateutil.parser
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

# TODO: connect to a local postgresql database --- (completed by Samuel Lartey)

db = SQLAlchemy(app)
from models import *

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. --- (completed by Samuel Lartey)
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue. --- (completed by Samuel Lartey)
    
  venues = Venue.query.all()
  data = []

  for venue in venues:
    num_upcoming_shows = Venue.query.join(shows_table).filter(Venue.id==venue.id).filter(shows_table.c.start_date > datetime.now()).count()

    new_data = {
      'city': venue.city,
      'state': venue.state,
      'venues': [{
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': num_upcoming_shows,
      }]
    }

    if len(data) == 0:
      data.append(new_data)
      continue
    
    size = 0
    for item in data:
      if item['city']==new_data['city'] and item['state']==new_data['state']:
        item['venues'].extend(new_data['venues'])
        break
      else:
        size += 1
        if size == len(data):
          data.append(new_data)

  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" --- (completed by Samuel Lartey)
  term = request.form.get('search_term', '')
  term = '%'+term+'%'
  queried_data = db.session.query(Venue).filter(Venue.name.ilike(term)).all()
  response={
    "count": len(queried_data),
    "data": queried_data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id --- (completed by Samuel Lartey)
  
  venue = Venue.query.filter(Venue.id==venue_id).first()

  past_shows_list = []
  past_shows = db.session.query(Artist.id, Artist.name, Artist.image_link, shows_table.c.start_date) \
    .select_from(shows_table).join(Artist, shows_table.c.artist_id==Artist.id) \
      .join(Venue, shows_table.c.venue_id==Venue.id) \
        .filter(Venue.id==venue.id) \
          .filter(shows_table.c.start_date < datetime.now()) \
            .all()

  for item in past_shows:
    add_show = {
      'artist_id': item[0],
      'artist_name': item[1],
      'artist_image_link': item[2],
      'start_time': str(item[3])
    }
    past_shows_list.append(add_show)
  

  upcoming_shows_list = []
  upcoming_shows = db.session.query(Artist.id, Artist.name, Artist.image_link, shows_table.c.start_date) \
    .select_from(shows_table).join(Artist, shows_table.c.artist_id==Artist.id) \
      .join(Venue, shows_table.c.venue_id==Venue.id) \
        .filter(Venue.id==venue.id) \
          .filter(shows_table.c.start_date > datetime.now()) \
            .all()
  
  for item in upcoming_shows:
    add_show = {
      'artist_id': item[0],
      'artist_name': item[1],
      'artist_image_link': item[2],
      'start_time': str(item[3])
    }
    upcoming_shows_list.append(add_show)

  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genres,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'address': venue.address,
    'website': venue.website_link,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.looking_for_talent,
    'image_link': venue.image_link,
    'past_shows': past_shows_list,
    'upcoming_shows': upcoming_shows_list,
    'past_shows_count': len(past_shows_list),
    'upcoming_shows_count': len(upcoming_shows_list),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead --- (completed by Samuel Lartey)
  # TODO: modify data to be the data object returned from db insertion --- (completed by Samuel Lartey)
  try:    
    print(True if request.form.get('seeking_talent') == "y" else False) # for debugging
    
    venue = Venue(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      genres = request.form['genres'],
      facebook_link = request.form['facebook_link'],
      image_link = request.form['image_link'],
      website_link = request.form['website_link'],
      looking_for_talent = True if request.form.get('seeking_talent') == "y" else False,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print(request.form.get('seeking_talent')) # for debugging
    print(e) # for debuggin
    # TODO: on unsuccessful db insert, flash an error instead. -- (completed by Samuel Lartey)
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using --- (completed by Samuel Lartey)
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter(Venue.id==venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database --- (completed by Samuel Lartey)
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band". --- (completed by Samuel Lartey)
  term = request.form.get('search_term', '')
  term = '%'+term+'%'
  queried_data = db.session.query(Artist).filter(Artist.name.ilike(term)).all()
  response={
    "count": len(queried_data),
    "data": queried_data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id --- (completed by Samuel Lartey)
  artist = Artist.query.filter(Artist.id==artist_id).first()

  past_shows_list = []
  past_shows = db.session.query(Venue.id, Venue.name, Venue.image_link, shows_table.c.start_date) \
    .select_from(shows_table).join(Artist, shows_table.c.artist_id==Artist.id) \
      .join(Venue, shows_table.c.venue_id==Venue.id) \
        .filter(Artist.id==artist.id) \
          .filter(shows_table.c.start_date < datetime.now()) \
            .all()

  for item in past_shows:
    add_show = {
      'venue_id': item[0],
      'venue_name': item[1],
      'venue_image_link': item[2],
      'start_time': str(item[3])
    }
    past_shows_list.append(add_show)
  
  upcoming_shows_list = []
  upcoming_shows = db.session.query(Venue.id, Venue.name, Venue.image_link, shows_table.c.start_date) \
    .select_from(shows_table).join(Artist, shows_table.c.artist_id==Artist.id) \
      .join(Venue, shows_table.c.venue_id==Venue.id) \
        .filter(Artist.id==artist.id) \
          .filter(shows_table.c.start_date > datetime.now()) \
            .all()
  
  for item in upcoming_shows:
    add_show = {
      'venue_id': item[0],
      'venue_name': item[1],
      'venue_image_link': item[2],
      'start_time': str(item[3])
    }
    upcoming_shows_list.append(add_show)

  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website_link,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'image_link': artist.image_link,
    'past_shows': past_shows_list,
    'upcoming_shows': upcoming_shows_list,
    'past_shows_count': len(past_shows_list),
    'upcoming_shows_count': len(upcoming_shows_list),
  }

  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # TODO: populate form with fields from artist with ID <artist_id> --- (completed by Samuel Lartey)
  artist = Artist.query.filter(Artist.id == artist_id).first()
  form.name.data = artist.name,
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
    
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes --- (completed by Samuel Lartey)
  try:
    artist = Artist.query.filter(Artist.id == artist_id).first()
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form['genres']
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website_link = request.form['website_link']
    artist.seeking_venue = True if request.form.get('seeking_venue') == "y" else False
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()  
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  # TODO: populate form with values from venue with ID <venue_id> --- (completed by Samuel Lartey)
  venue = Venue.query.filter(Venue.id == venue_id).first()
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.looking_for_talent
  form.seeking_description.data = venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes --- (completed by Samuel Lartey)
  try:
    venue = Venue.query.filter(Venue.id == venue_id).first()
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.genres = request.form['genres']
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website_link = request.form['website_link']
    venue.seeking_talent = True if request.form.get('seeking_talent') == "y" else False
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()  
  return redirect(url_for('show_venue', venue_id=venue_id))
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead --- (completed by Samuel Lartey)
  # TODO: modify data to be the data object returned from db insertion --- (completed by Samuel Lartey)
  try:
    artist = Artist(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      genres = request.form['genres'],
      facebook_link = request.form['facebook_link'],
      image_link = request.form['image_link'],
      website_link = request.form['website_link'],
      seeking_venue = True if request.form.get('seeking_venue') == "y" else False,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print(e)
    # TODO: on unsuccessful db insert, flash an error instead. -- (completed by Samuel Lartey)
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. --- (completed by Samuel Lartey)
  query = db.session.query(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, shows_table.c.start_date) \
    .select_from(shows_table).join(Venue, Venue.id == shows_table.c.venue_id).join(Artist, Artist.id==shows_table.c.artist_id) \
      .all()
  
  data = []

  for q in query:
    new_entry = {
      'venue_id': q[0],
      'venue_name': q[1],
      'artist_id': q[2],
      'artist_name': q[3],
      'artist_image_link': q[4],
      'start_time': str(q[5])
    }
    data.append(new_entry)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead --- (completed by Samuel Lartey)
  try:
    
    artist = Artist.query.filter(Artist.id==request.form['artist_id']).first()
    venue = Venue.query.filter(Venue.id==request.form['venue_id']).first()
    start_time = request.form['start_time']
    # artist.venues.append(venue)
    show = shows_table.insert().values(artist_id=artist.id, venue_id=venue.id, start_date=start_time)
    db.session.execute(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print(e)
    # TODO: on unsuccessful db insert, flash an error instead. -- (completed by Samuel Lartey)
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2022))
    app.debug=True
    app.run(host='0.0.0.0', port=port)

