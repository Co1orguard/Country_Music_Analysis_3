from flask_wtf import FlaskForm
from typing import List, Tuple
from wtforms import SubmitField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from applayer.artistlist import ArtistList
from datalayer.artistnotfound import ArtistNotFound


class ExpansionForm(FlaskForm):
    # The next four lines are the extension point for adding data to the pick list
    choices: List[Tuple[int, str]]
    ids = []
    try:
        artists = ArtistList(ids)
        choices = artists.artists
    except ArtistNotFound:
        choices = None
    # Create the two fields for the form
    expanse_select = SelectMultipleField("Select artists to expand", choices=choices, coerce=int)
#    submit = SubmitField('Expand Selected')

    def __init__(self, choices, *args, **kwargs):
        super(ExpansionForm, self).__init__(*args, **kwargs)
        self.expanse_select.choices = choices

