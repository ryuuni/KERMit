from server.server import db, app  # db object from the file where db connection was initialized
import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = self.hash_password(password)

    @classmethod
    def find_by_username(cls, username):
        """
        Returns the User from the database associated with the username.
        If the username does not exist, None will be returned
        """
        return cls.query.filter_by(username=username).first()

    def save(self):
        """
        Saves User to the database.
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def hash_password(pt_password):
        """
        Hash a password for the first name; salt is saved into the hash itself. Salting the
        password ensures that the hash algorithm's outcome is not longer predictable; in other words,
        the same password will no longer yield the same hash.
        """
        salt = bcrypt.gensalt(app.config.get('BCRYPT_SALT_ROUNDS'))
        return bcrypt.hashpw(pt_password, salt)

    def check_password(self, pt_password):
        """
        Checks the plaintext password provided against the hashed password stored for the user.
        """
        return bcrypt.checkpw(pt_password, self.hashed_password)

    def __str__(self):
        return f'User(username={self.username}, id={self.id})'
