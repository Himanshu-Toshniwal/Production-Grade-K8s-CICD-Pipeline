from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different username.')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    image_url = StringField('Image URL', validators=[Length(max=500)])
    category = SelectField('Category', choices=[
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Home', 'Home'),
        ('Sports', 'Sports'),
        ('Books', 'Books'),
        ('Toys', 'Toys')
    ])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    features = TextAreaField('Features (comma-separated)')

class CheckoutForm(FlaskForm):
    shipping_name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    shipping_email = StringField('Email', validators=[DataRequired(), Email()])
    shipping_phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    shipping_address = TextAreaField('Address', validators=[DataRequired()])
    shipping_city = StringField('City', validators=[DataRequired(), Length(max=100)])
    shipping_state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    shipping_zip = StringField('ZIP/Postal Code', validators=[DataRequired(), Length(max=20)])
    shipping_country = StringField('Country', validators=[DataRequired(), Length(max=100)])

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Review', validators=[Length(max=1000)])

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
