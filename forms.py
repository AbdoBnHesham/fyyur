from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    TextAreaField
)
from wtforms.validators import DataRequired, URL, Optional, Regexp

from enums import State


class ShowForm(FlaskForm):
    def __init__(self, artists_choices, venues_choices, **kwargs):
        super().__init__(**kwargs)
        self.artist_id.choices = artists_choices
        self.venue_id.choices = venues_choices

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


class BaseForm(object):
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
    phone = StringField(
        'phone',
        # Maybe some one don't want to share his phone for any reason
        # I'm using regex to make sure it matches the pattern 111-111-1111
        validators=[
            Optional(),
            Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{4}$',
                   message="number should match this pattern 111-111-1111")
        ]
    )
    image_link = StringField(
        'image_link',
        validators=[DataRequired(), URL()]
    )
    facebook_link = StringField(
        # Maybe there is no facebook account for this venue
        'facebook_link',
        validators=[Optional(), URL()]
    )
    website = StringField(
        # Maybe there is no website for this venue
        'website',
        validators=[Optional(), URL()]
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
        choices=[]
    )


class VenueForm(FlaskForm, BaseForm):
    def __init__(self, genres_choices, **kwargs):
        super().__init__(**kwargs)
        self.genres_ids.choices = genres_choices

    address = StringField(
        'address',
        validators=[DataRequired()]
    )


class ArtistForm(FlaskForm, BaseForm):
    def __init__(self, genres_choices, **kwargs):
        super().__init__(**kwargs)
        self.genres_ids.choices = genres_choices
