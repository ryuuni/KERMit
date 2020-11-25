"""
Contents include the implementation of the User class, which holds information
about a User registered with the puzzle system. User information used
to populate this table comes from information retrieved from the Google OAuth API.
"""
from backend import db


class User(db.Model):
    """
    Class which holds contents about puzzle users.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_id = db.Column(db.String(25), nullable=False, unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False)

    def __init__(self, g_id, first_name, last_name, email):
        self.g_id = g_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @classmethod
    def find_by_g_id(cls, g_id):
        """
        Returns the User from the database associated with the specific google id.
        If the username does not exist, None will be returned
        """
        return cls.query.filter_by(g_id=g_id).first()

    @classmethod
    def find_users_by_email(cls, emails):
        """
        Given a list of user emails, find the users associated with the emails.
        Function returns tuple of the list of "found" users and a list of emails
        that were not found in the system.
        """
        found = []
        not_found = []

        for email in emails:
            user = cls.find_by_email(email)
            if user is not None:
                found.append(user)
            else:
                not_found.append(email)

        return found, not_found

    @classmethod
    def find_by_email(cls, email):
        """
        Finds a User by their email address; if email address it not
        registered, then None will be returned.
        """
        return cls.query.filter_by(email=email).first()

    def save(self):
        """
        Saves User to the database.
        """
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f'User(first_name={self.first_name}, last_name={self.last_name}, id={self.id})'

    def as_str(self):
        """
        String conversion of User for specific formatting use cases.
        """
        return f"{self.first_name} {self.last_name} (id = {self.id})"
