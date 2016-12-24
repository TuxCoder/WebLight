from flask_login import AnonymousUserMixin, UserMixin
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Returns a user object by given ID."""
    return User.query.get(int(user_id))


class Permission:
    """Permission Bitmask required for the Role table."""
    SOLVE = 0x01
    WRITE_BLOG = 0x02
    ADMINISTER = 0x80


class User(UserMixin, db.Model):
    """Users which are able to gather points and log in.

    :param int user_id: Unique ID and primary key
    :param text login_name: Human readable name
    :param text password_hash: Hashed password
    :param DateTime last_login: Date and Time of the last login
    :param bool active: True, if user is visible and able to login, else False
    :param int role_id: Role ID assigned with this user
    :param Challenge challenges: All challenges solved by this user
    :param Post posts: All posts written by this user
    """
    __tablename__ = "AppUser"
    user_id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    last_login = db.Column(db.DateTime)
    active = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.INT, nullable=False, default=0)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return '{}'.format(self.login_name)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.login_name)

    def get_id(self):
        """Returns the unique identifier

        Required by flask-login
        """
        return self.user_id

    @property
    def password(self):
        """The password property itself should not be accessible."""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Generates a password hash.

        :param str password: Cleartext password to hash
        """
        self.password_hash = generate_password_hash(password)

    def is_active(self):
        """Checks if the user is activated.

        Only activated users are able to log in and perform tasks appropriate
        to their permissions.

        This function is required by flask-login. If this function gets
        deleted it will be replaced by a default function inherited from
        UserMixin.
        """
        return self.active

    def verify_password(self, password):
        """Verifies the password against the stored hash.

        :param str password: Cleartext password to check

        Returns True if both hash and cleartext password match.
        """
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        """Checks permissions.

        :param Permission permissions: permissions

        Returns True if user has given permissions.
        """
        return (self.role & permissions) == permissions

    def is_administrator(self):
        """Checks against Administrator permission.

        Returns True if user has ADMINISTER permissions.
        """
        return self.can(Permission.ADMINISTER)


class AnonymousUser(AnonymousUserMixin):
    """Anonymous user required by flask-login extension."""

    def can(self, permissions):
        """Anonymous user has no permissions."""
        return False

    def is_administrator(self):
        """Anonymous user has no administration rights."""
        return False


login_manager.anonymous_user = AnonymousUser
