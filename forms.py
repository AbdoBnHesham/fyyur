from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional, Regexp

states = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]


class ShowForm(FlaskForm):
    artist_id = SelectField(  # using select to make sure it exists and for better UX
        'artist_id',
        validators=[DataRequired()],
        choices=[],  # dynamically set
    )
    venue_id = SelectField(  # using select to make sure it exists and for better UX
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
        choices=states
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
        # TODO implement enum restriction               # I don't understand
        'facebook_link',
        validators=[Optional(), URL()]  # Maybe there is no facebook account for this venue
    )
    website = StringField(
        'website',
        validators=[Optional(), URL()]  # Maybe there is no website for this venue
    )
    seeking_description = TextAreaField(
        'seeking_description',
        validators=[Optional()]  # it can be empty
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction               # I don't understand but I have done it with choices from db
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
