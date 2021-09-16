from flask_login import UserMixin
from datetime import datetime

from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
class Movie:
    '''
    Movie class to define Movie Objects
    '''

    def __init__(self,id,title,overview,poster,vote_average,vote_count):
        self.id =id
        self.title = title
        self.overview = overview
        self.poster = "https://image.tmdb.org/t/p/w500/" + poster
        self.vote_average = vote_average
        self.vote_count = vote_count


        
class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    movie_id = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    image_path = db.Column(db.String)
    movie_review = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(movie_id=id).all()
        return reviews


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

class User(UserMixin,db.Model):
    """
    This is a class that defines the structure of a user
    
    Args: 
        db.Model: This will connect our class and our database
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        """This is to make sure one cannot read the password

        Raises:
            AttributeError: [That one cannot read the attribute]
        """
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        """This creates the hashed version of a password

        Args:
            password ([any]): [This takes in the password provided]
        """
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        """This is to verify the hashed password with the one stored in the database

        Args:
            password (any): [takes in the password and checks it against the hashed password]

        Returns:
            [boolean]: [Whether or not the passwords match]
        """
        return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
        """
        This helps in debugging
        """
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'
