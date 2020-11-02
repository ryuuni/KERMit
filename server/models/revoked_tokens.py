from server.server import db


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
