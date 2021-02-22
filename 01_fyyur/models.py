from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


db = SQLAlchemy()
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
        upcoming_shows = db.session.query(Artist).with_entities(Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label(
            'artist_image_link'), Show.start_time.label('start_time')).join(Show).filter((Show.venue_id == self.id), (Show.start_time > datetime.now())).all()
        return [{"artist_id": upcoming_show.artist_id,
                 "artist_name": upcoming_show.artist_name,
                 "artist_image_link": upcoming_show.artist_image_link,
                 "start_time": upcoming_show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'} for upcoming_show in upcoming_shows]

    def past_shows(self):
        upcoming_shows = db.session.query(Artist).with_entities(Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label(
            'artist_image_link'), Show.start_time.label('start_time')).join(Show).filter((Show.venue_id == self.id), (Show.start_time <= datetime.now())).all()
        return [{"artist_id": upcoming_show.artist_id,
                 "artist_name": upcoming_show.artist_name,
                 "artist_image_link": upcoming_show.artist_image_link,
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
        upcoming_shows = db.session.query(Venue).with_entities(Venue.id.label('venue_id'), Venue.name.label('venue_name'), Venue.image_link.label(
            'venue_image_link'), Show.start_time.label('start_time')).join(Show).filter((Show.artist_id == self.id), (Show.start_time > datetime.now())).all()
        return [{"venue_id": upcoming_show.venue_id,
                 "venue_name": upcoming_show.venue_name,
                 "venue_image_link": upcoming_show.venue_image_link,
                 "start_time": upcoming_show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'} for upcoming_show in upcoming_shows]

    def past_shows(self):
        upcoming_shows = db.session.query(Venue).with_entities(Venue.id.label('venue_id'), Venue.name.label('venue_name'), Venue.image_link.label(
            'venue_image_link'), Show.start_time.label('start_time')).join(Show).filter((Show.artist_id == self.id), (Show.start_time <= datetime.now())).all()
        return [{"venue_id": upcoming_show.venue_id,
                 "venue_name": upcoming_show.venue_name,
                 "venue_image_link": upcoming_show.venue_image_link,
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
