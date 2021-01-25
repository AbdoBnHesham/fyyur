from datetime import datetime

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


def setup_db(app):
    db.app = app
    db.init_app(app)
    return db


class Show(db.Model):
    query: BaseQuery
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer,
                          db.ForeignKey('artists.id', ondelete='CASCADE'))
    venue_id = db.Column(db.Integer,
                         db.ForeignKey('venues.id', ondelete='CASCADE'))
    start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship(
        'Artist',
        lazy=True,
        backref=db.backref('shows_relation', lazy='dynamic',
                           cascade="all, delete")
    )
    venue = db.relationship(
        'Venue',
        lazy=True,
        backref=db.backref('shows_relation', lazy='dynamic',
                           cascade="all, delete")
    )

    @hybrid_property
    def artist_name(self):
        return self.artist.name

    @hybrid_property
    def artist_image_link(self):
        return self.artist.image_link

    @hybrid_property
    def venue_name(self):
        return self.venue.name

    @hybrid_property
    def venue_image_link(self):
        return self.venue.image_link

    def __repr__(self):
        v_name = self.venue_name
        a_name = self.artist_name
        return f'<Show venue_name:{v_name} artist_name:{a_name}>'


# Adding Genre as a table for possible needs of adding more
# for an non-programmer administrator
class Genre(db.Model):
    query: BaseQuery
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)

    @staticmethod
    def genres_choices():
        return [(str(x.id), x.name) for x in
                db.session.query(Genre.id, Genre.name).order_by('name')]

    @staticmethod
    def get_genres_by_ids(ids: list):
        return db.session.query(Genre).filter(Genre.id.in_(ids)).all()

    def __repr__(self):
        return f"<Genre {self.id} {self.name}>"


genres_venues = db.Table(
    'genres_venues',
    db.Column('genre_id', db.Integer,
              db.ForeignKey('genres.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('venue_id', db.Integer,
              db.ForeignKey('venues.id', ondelete='CASCADE'),
              primary_key=True),
)

genres_artists = db.Table(
    'genres_artists',
    db.Column('genre_id', db.Integer,
              db.ForeignKey('genres.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('artist_id', db.Integer,
              db.ForeignKey('artists.id', ondelete='CASCADE'),
              primary_key=True),
)


class HybridShowsMixin(object):
    @hybrid_property
    def shows(self):
        return self.shows_relation.all()

    @hybrid_property
    def shows_count(self):
        return self.shows_relation.count()

    @hybrid_property
    def upcoming_shows(self):
        return self.shows_relation.filter(
            Show.start_time >= datetime.now()).all()

    @hybrid_property
    def upcoming_shows_count(self):
        return self.shows_relation.filter(
            Show.start_time >= datetime.now()).count()

    @hybrid_property
    def past_shows(self):
        return self.shows_relation.filter(
            Show.start_time <= datetime.now()).all()

    @hybrid_property
    def past_shows_count(self):
        return self.shows_relation.filter(
            Show.start_time <= datetime.now()).count()


class HybridGenresMixin(object):
    @hybrid_property
    def genres(self):
        return [g.name for g in self.genres_relation]

    @hybrid_property
    def genres_ids(self):
        return [str(g.id) for g in self.genres_relation]

    @genres_ids.setter
    def genres_ids(self, ids):
        self.genres_relation = Genre.get_genres_by_ids(ids)


class Venue(db.Model, HybridShowsMixin, HybridGenresMixin):
    query: BaseQuery
    __tablename__ = 'venues'
    # it's only used to get id its from the URI combined with _id
    __model_name__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True, unique=True)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True, unique=True)
    website = db.Column(db.String(120), nullable=True, unique=True)
    seeking_description = db.Column(db.String(1000), nullable=True)
    genres_relation = db.relationship('Genre', secondary=genres_venues,
                                      lazy='joined')

    @hybrid_property
    def seeking_talent(self):
        s = self.seeking_description
        return s is not None and s

    @staticmethod
    def venues_choices():
        return [
            (str(v.id), f"ID:{v.id} {v.name}") for v in
            db.session.query(Venue.id, Venue.name).order_by(Venue.id)
        ]

    def __repr__(self):
        return f"<Venue {self.id} {self.name}>"


class Artist(db.Model, HybridShowsMixin, HybridGenresMixin):
    query: BaseQuery
    __tablename__ = 'artists'
    # it's only used to get id its from the URI combined with _id
    __model_name__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True, unique=True)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True, unique=True)
    website = db.Column(db.String(120), nullable=True, unique=True)
    seeking_description = db.Column(db.String(1000), nullable=True)
    genres_relation = db.relationship('Genre', secondary=genres_artists,
                                      lazy='joined')

    @hybrid_property
    def seeking_venue(self):
        s = self.seeking_description
        return s is not None and s

    @staticmethod
    def artists_choices():
        return [
            (str(a.id), f"ID:{a.id} {a.name}") for a in
            db.session.query(Artist.id, Artist.name).order_by(Artist.id)
        ]

    def __repr__(self):
        return f"<Artist {self.id} {self.name}>"
