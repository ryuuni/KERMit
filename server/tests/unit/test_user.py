from server.server import app, db     # this dependency is necessary to prevent a circular import
from server.models.user import User
from server.config import UnitTestingConfig

app.config.from_object(UnitTestingConfig)


def test_create_user():
    user = User('103207743267402488580', 'Megan', 'Frenkel', 'mmf2171@columbia.edu')
    assert user.last_name == 'Frenkel'
    assert user.first_name == 'Megan'
    assert user.email == 'mmf2171@columbia.edu'
    assert user.g_id == '103207743267402488580'
