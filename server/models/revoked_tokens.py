"""
Inspiration for this approach to handling revoked tokens from Oleg Agapov.
Source: Agapov, O., "JWT authorization in Flask", codeburst.io, Medium.com,
        accessed November 2, 2020 at https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
"""
from server.server import db  # db object from the file where db connection was initialized


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
        Checks to determine if the token has is on the token 'blacklist'.
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
