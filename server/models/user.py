from server.server import db


class User(db.Model):
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

    def save(self):
        """
        Saves User to the database.
        """
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f'User(first_name={self.first_name}, last_name={self.last_name})'

    def as_str(self):
        return f"{self.first_name} {self.last_name} (id = {self.id})"

