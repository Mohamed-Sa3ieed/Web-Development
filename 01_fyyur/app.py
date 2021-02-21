#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from datetime import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from itertools import groupby
from operator import attrgetter
#from models import Venue,Artist,Show,Album,Song,db
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db.init_app(app)
# Done: connect to a local postgresql database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy='joined')

    def __repr__(self):
        return f'< Venue: id: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, genres: {self.genres} , image_link:{self.image_link}, website:{self.website}, facebook_link:{self.facebook_link}, seeking_talent:{self.seeking_talent}, seeking_description:{self.seeking_description}, shows:{self.shows}>'

    def upcoming_shows(self):
        upcoming_shows = Show.query.filter(
            (Show.venue_id == self.id), (Show.start_time > datetime.now())).all()
        return [{"artist_id": upcoming_show.artist_id,
                 "artist_name": upcoming_show.artist.name,
                 "artist_image_link": upcoming_show.artist.image_link,
                 "start_time": upcoming_show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'} for upcoming_show in upcoming_shows]

    def past_shows(self):
        upcoming_shows = Show.query.filter(
            (Show.venue_id == self.id), (Show.start_time <= datetime.now())).all()
        return [{"artist_id": upcoming_show.artist_id,
                 "artist_name": upcoming_show.artist.name,
                 "artist_image_link": upcoming_show.artist.image_link,
                 "start_time": upcoming_show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'} for upcoming_show in upcoming_shows]

    # Done: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    albums = db.relationship('Album', backref='artist', lazy=True)
    songs = db.relationship('Song', backref='artist', lazy=True)
    shows = db.relationship('Show', backref='artist', lazy='joined')

    def __repr__(self):
        return f'< Artist: id: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link:{self.image_link}, website:{self.website}, facebook_link:{self.facebook_link}, seeking_venue:{self.seeking_venue}, seeking_description:{self.seeking_description}, shows:{self.shows}>'
    # Done: implement any missing fields, as a database migration using Flask-Migrate

    def upcoming_shows(self):
        upcoming_shows = Show.query.filter(
            (Show.artist_id == self.id), (Show.start_time > datetime.now())).all()
        return [{"venue_id": upcoming_show.venue_id,
                 "venue_name": upcoming_show.venue.name,
                 "venue_image_link": upcoming_show.venue.image_link,
                 "start_time": upcoming_show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'} for upcoming_show in upcoming_shows]

    def past_shows(self):
        upcoming_shows = Show.query.filter(
            (Show.artist_id == self.id), (Show.start_time <= datetime.now())).all()
        return [{"venue_id": upcoming_show.venue_id,
                 "venue_name": upcoming_show.venue.name,
                 "venue_image_link": upcoming_show.venue.image_link,
                 "start_time": upcoming_show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'} for upcoming_show in upcoming_shows]


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(), nullable=False)
    songs = db.relationship('Song', backref='album', lazy=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey(
        'albums.id'), nullable=False)


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)

    def __repr__(self):
        return f'<Show: id:{self.id}, start_time:{self.start_time}, artist_id:{self.artist_id}, venue_id:{self.venue_id}>'


# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='EN')


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
    # Done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    results = Venue.query.order_by(Venue.state,Venue.city).all()
    results = [[k, list(g)] for k, g in groupby(
        results, attrgetter('state', 'city'))]
    data = []
    for grp in results:
        data_record = {
            "state": grp[0][0],
            "city": grp[0][1],
        }
        venues_details = []
        for venue_data in grp[1]:
            venues_details.append({
                "id": venue_data.id,
                "name": venue_data.name,
                "num_upcoming_shows": len(venue_data.upcoming_shows())
            })
        data_record['venues'] = venues_details
        data.append(data_record)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    error = False
    response = {}
    try:
        search_string = request.form.get("search_term")
        results = Venue.query.filter(
            Venue.name.like('%'+search_string+'%')).all()
        data = [{
                "id": result.id,
                "name": result.name,
                "num_upcoming_shows": len(result.upcoming_shows())
                } for result in results]
        response = {
            "count": len(results),
            "data": data
        }
    except:
        error = True
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()
    if not error:
        return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # Done: replace with real venue data from the venues table, using venue_id
    error = False
    data = {}
    try:
        result = Venue.query.get(venue_id)
        past_shows = result.past_shows()
        upcoming_shows = result.upcoming_shows()
        data = {
            "id": result.id,
            "name": result.name,
            "genres": result.genres.replace('{', '').replace('}', '').split(','),
            "address": result.address,
            "city": result.city,
            "state": result.state,
            "phone": result.phone,
            "website": result.website,
            "facebook_link": result.facebook_link,
            "seeking_talent": result.seeking_talent,
            "seeking_description": result.seeking_description,
            "image_link": result.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }
    except:
        error = True
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()
    if not error:
        return render_template('pages/show_venue.html', venue=data)
    else:
        return render_template('error/404.html')

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    # form = VenueForm(request.form,obj=)
    form = VenueForm(request.form)
    try:
        venue = Venue()
        form.populate_obj(venue)
        # Done: insert form data as a new Venue record in the db, instead
        db.session.add(venue)
        print(venue)
        db.session.commit()
        # Done: modify data to be the data object returned from db insertion
        form = VenueForm(obj=venue)
    except Exception as e:
        print(str(e))
        # Done: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        error = True
        db.session.rollback()
        print(str(sys.exc_info))
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Done: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    data = {}
    try:
        Venue.query.filter(Venue.id == venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()
    if not error:
        return redirect(url_for('index'))
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # Done: replace with real data returned from querying the database
    data = [{"id": artist.id, "name": artist.name}
            for artist in Artist.query.with_entities(Artist.id, Artist.name).all()]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    error = False
    response = {}
    try:
        search_string = request.form.get("search_term")
        results = Artist.query.filter(
            Artist.name.like('%'+search_string+'%')).all()
        data = [{
                "id": result.id,
                "name": result.name,
                "num_upcoming_shows": len(result.upcoming_shows())
                } for result in results]
        response = {
            "count": len(results),
            "data": data
        }
    except:
        error = True
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()
    if not error:
        return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # Done: replace with real venue data from the venues table, using venue_id
    error = False
    data = {}
    try:
        result = Artist.query.get(artist_id)
        past_shows = result.past_shows()
        upcoming_shows = result.upcoming_shows()
        data = {
            "id": result.id,
            "name": result.name,
            "genres": result.genres.replace('{', '').replace('}', '').split(','),
            "city": result.city,
            "state": result.state,
            "phone": result.phone,
            "website": result.website,
            "facebook_link": result.facebook_link,
            "seeking_venue": result.seeking_venue,
            "seeking_description": result.seeking_description,
            "image_link": result.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }
    except:
        error = True
        db.session.rollback()
        abort(404)
    finally:
        db.session.close()
    if not error:
        return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist=Artist.query.get(artist_id)
    # Done: populate form with fields from artist with ID <artist_id>
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    # Done: take values from the form submitted, and update existing
    form = ArtistForm(request.form)
    try:
        # artist record with ID <artist_id> using the new attributes
        artist = Artist.query.get(artist_id)
        form.populate_obj(artist)
        # Done: insert form data as a new Venue record in the db, instead
        db.session.add(artist)
        db.session.commit()
        # Done: modify data to be the data object returned from db insertion
        form=ArtistForm(obj=artist)
    except Exception as e:
        print(str(e))
        # Done: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
        error = True
        db.session.rollback()
        print(str(sys.exc_info))
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # Done: populate form with values from venue with ID <venue_id>
    venue=Venue.query.get(venue_id)
    form=VenueForm(obj=venue)
    
    return render_template('forms/edit_venue.html', form=form,venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    
    error = False
    # Done: take values from the form submitted, and update existing
    form = VenueForm(request.form)
    try:
        venue = Venue.query.get(venue_id)
        form.populate_obj(venue)
        # Done: insert form data as a new Venue record in the db, instead
        db.session.add(venue)
        print(venue)
        db.session.commit()
        # Done: modify data to be the data object returned from db insertion
        form = VenueForm(obj=venue)
    except Exception as e:
        print(str(e))
        # Done: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
        error = True
        db.session.rollback()
        print(str(sys.exc_info))
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
        # venue record with ID <venue_id> using the new attributes
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
    error = False
    # form = VenueForm(request.form,obj=)
    form = ArtistForm(request.form)
    try:
        artist = Artist()
        form.populate_obj(artist)
        # Done: insert form data as a new Venue record in the db, instead
        db.session.add(artist)
        db.session.commit()
        # Done: modify data to be the data object returned from db insertion
        form=ArtistForm(obj=artist)
    except Exception as e:
        print(str(e))
        # Done: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        error = True
        db.session.rollback()
        print(str(sys.exc_info))
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # Done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.order_by(Show.start_time).all()
    data = [{
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
    } for show in shows]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    # form = VenueForm(request.form,obj=)
    form = ShowForm(request.form)
    try:
        show = Show()
        form.populate_obj(show)
        # Done: insert form data as a new Venue record in the db, instead
        db.session.add(show)
        print(show)
        db.session.commit()
        # Done: modify data to be the data object returned from db insertion
        form = ShowForm(obj=show)
    except Exception as e:
        print(str(e))
        # Done: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show at ' + request.form['start_time'] + ' could not be listed.')
        error = True
        db.session.rollback()
        print(str(sys.exc_info))
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    return render_template('forms/new_show.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
