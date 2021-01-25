from datetime import datetime

from flask import request
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField,
    SelectMultipleField, DateTimeField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired, URL,
    Optional, Regexp,
    ValidationError
)

from app import db
from enums import State
from models import Venue, Artist, Genre


def unique(model):
    """
        validate form filed is unique in for any model
        and making sure it ignore it's own value in case of editing
    """

    def _unique(form, field):
        _id = request.view_args.get(f'{model.__model_name__}_id', None)
        exists = False
        if field.data:
            exists = db.session.query(
                model.query.filter(
                    vars(model)[field.name] == field.data,
                    model.id != _id
                ).exists()
            ).scalar()
        if exists:
            raise ValidationError(f'This {field.name} has been used')

    return _unique


def string_or_none(form, field):
    """
        making sure value the value is none for those cases where it's unique
        and nullable
        of course only if it's empty string
    """
    field.data = field.data if field.data else None


class ShowForm(FlaskForm):
    artist_id = SelectField(
        # using select to make sure it exists and for better UX
        'artist_id',
        validators=[DataRequired()],
        choices=[],
    )
    venue_id = SelectField(
        # using select to make sure it exists and for better UX
        'venue_id',
        validators=[DataRequired()],
        choices=[],
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.now(),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Need to set it on every init as it's not a constant value
        self.artist_id.choices = Artist.artists_choices()
        self.venue_id.choices = Venue.venues_choices()


class BaseForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    city = StringField(
        'city',
        validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=State.choices()
    )
    image_link = StringField(
        'image_link',
        validators=[DataRequired(), URL()]
    )
    seeking_description = TextAreaField(
        'seeking_description',
        validators=[Optional()]  # it can be empty
    )
    genres_ids = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        # make sure to run migration with flask db upgrade
        # as it will add initial data to genres table
        choices=[],
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Need to set it on every init as it's not constant
        # For this case actually it's constant but it's good for future
        self.genres_ids.choices = Genre.genres_choices()


# I'm using regex to make sure it matches the pattern 111-111-1111
phone_regex = Regexp(
    '^[0-9]{3}-[0-9]{3}-[0-9]{4}$',
    message="number should match this pattern 111-111-1111"
)


class VenueForm(BaseForm):
    address = StringField(
        'address',
        validators=[DataRequired()]
    )
    phone = StringField(
        'phone',
        validators=[
            string_or_none,
            Optional(),
            phone_regex,
            unique(Venue)
        ]
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[string_or_none, Optional(), URL(), unique(Venue)]
    )
    website = StringField(
        'website',
        validators=[string_or_none, Optional(), URL(), unique(Venue)]
    )


class ArtistForm(BaseForm):
    phone = StringField(
        'phone',
        validators=[
            string_or_none,
            Optional(),
            phone_regex,
            unique(Artist)
        ]
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[string_or_none, Optional(), URL(), unique(Artist)]
    )
    website = StringField(
        'website',
        validators=[string_or_none, Optional(), URL(), unique(Artist)]
    )
