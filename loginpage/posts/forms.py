from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
    bins = SelectField('Disposal Method', choices=[('Green Bin', 'Papier'), ('Blue Bin', 'Glas'),
                                                   ('Gelber Sack', 'Packaging Recycling'),
                                                   ('Restmull Bin', 'Residual Waste'),
                                                   ('Brown Bin', 'Bio-waste'), ('E-waste Bin', 'Electronic Waste')])
    # bins = SelectField('Disposal Method', choices=[('Green Bin', 'BioWaste'), ('Grey Bin', 'Rest bin')])
    submit = SubmitField('Post')



class FindForm(FlaskForm):
    waste = StringField('What do you wanna dispose?', validators=[DataRequired()])
    submit = SubmitField('Find')

class BinsForm(FlaskForm):
    bin = SelectField('Which bin?', choices=[('Green Bin', 'Green Bin'), ('Blue Bin', 'Blue Bin'),
                                             ('Gelber Sack', 'Gelber Sack'), ('Restmull Bin', 'Restmull Bin'),
                                             ('Brown Bin', 'Brown Bin'), ('E-waste Bin', 'E-waste Bin')])
    submit = SubmitField('Find')

