from flask_security import LoginForm, RegisterForm
from flask_wtf import Form
from wtforms import BooleanField, PasswordField, validators, StringField, ValidationError, SelectField, SubmitField
from wtforms.fields.html5 import EmailField
from app.models import User, Feed


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username',[validators.DataRequired(message='username is required')])

    def validate(self):
        """ Add username validation

            :return: True is the form is valid
        """
        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            return False

        # Check if username already exists
        user = User.query.filter_by(
            username=self.username.data).first()
        if user is not None:
            # Text displayed to the user
            self.username.errors.append('Username already exists. Try a unique name that best describes you, like LadiesMan01.')
            return False

        return True

    remember = BooleanField('Remember Me')


class RegisterFeedForm(Form):
    feedTitle     = StringField('Feed Title', [validators.DataRequired(message='Title is required')])
    feedURL        = StringField('RSS/Atom URL', [validators.DataRequired(message='Feed\'s URL is required'),validators.URL(require_tld= True,message='Invalid URL')])
    feedCategory   = SelectField('Choose Category',[validators.DataRequired(message='Please Choose the appropriate category for the feed')],
                                 choices=[('Sports', 'Sports'), ('Business', 'Business'), ('Creative Writing', 'Creative Writing')])
    feedDescription = StringField('Feed Title', [validators.DataRequired(message='Please add a short description of the blog/site. At least 20 characters'), validators.length(min=20)])
    submit = SubmitField()

    def validate(self):
        """ Add username validation

            :return: True is the form is valid
        """
        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            return False

        # Check if username already exists
        feed = Feed.query.filter_by(
            feedURL = self.feedURL.data).first()
        if feed is not None:
            # Text displayed to the user
            self.feedURL.errors.append('Feed has already been registered. Maybe register another one?')
            return False

        print(self.feedURL.data)





    def validate(self):
        """ Add username validation

            :return: True is the form is valid
        """
        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            return False

        import feedparser
        parsed = feedparser.parse(self.feedURL.data)

        if parsed.entries == []:
            self.feedURL.errors.append('Feed doesnt appear to be valid. Trying adding /RSS or /feed at the end?')
        else:
            self.feedURL.errors.append('Feed doesnt appear to be valid. Trying adding /RSS or /feed at the end?')

        return True

'''
class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'Username is already taken!'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
'''


