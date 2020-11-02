from server.server import db  # db object from the file where db connection was initialized
import bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    def save(self):
        """
        Saves User to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def hash_password(pt_password):
        """
        Hash a password for the first name; salt is saved into the hash itself
        """
        return bcrypt.hashpw(pt_password, bcrypt.gensalt())

    @staticmethod
    def check_password(pt_password, hashed_password):
        return bcrypt.checkpw(pt_password, hashed_password)


class RevokedTokens(db.Model):

    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120), nullable=False, unique=True)
    token_type = db.Column(db.String(32))

    def add_to_blacklist(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Does a check to determine if the token has been revoked.
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
