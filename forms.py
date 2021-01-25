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
    artist_id = SelectField(
        # using select to make sure it exists and for better UX
        'artist_id',
        validators=[DataRequired()],
        choices=[],  # dynamically set
    )
    venue_id = SelectField(
        # using select to make sure it exists and for better UX
        'venue_id',
        validators=[DataRequired()],
        choices=[],  # dynamically set
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
        validators=[URL()]
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
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=[]  # Dynamically set
    )


class VenueForm(FlaskForm, BaseForm):
    address = StringField(
        'address',
        validators=[DataRequired()]
    )


class ArtistForm(FlaskForm, BaseForm):
    pass
