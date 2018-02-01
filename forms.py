from wtforms import Form, StringField, SelectField

class MusicSearchForm(Form):
    categories = [('Respiratory', 'Respiratory'),
               ('Cords', 'Cords'),
               ('Strengthening', 'Strengthening')]
    select = SelectField('Search for projects:', choices=choices)
    search = StringField('')
