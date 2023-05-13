from quiz_app.user_register import UserRegister
from werkzeug.security import generate_password_hash, check_password_hash


class User():

    # construct / attributes
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.passwordHash = passwordHash.replace("\'", "")
        self.is_authenticated = True
        self.is_active= True
        self.is_anonymous = False


    @staticmethod
    def login(username, password):

        with UserRegister as db:
            usr = db.getUser(username)
            if usr:
                user = User(*usr)
                pwd = user.passwordHash.replace("\'", "")
                if check_password_hash(pwd, password):
                    return True
            return False

    @staticmethod
    def register(username, password):

        with UserRegister() as db:
            usr = db.create_user(username, password)
            if usr:
                return True
            else: return False

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def __str__(self):
        return f'Id: {self.id}\n' + \
               f'Username: {self.userName}\n' + \
               f'Email: {self.email}\n' + \
               f'Password Hash: {self.passwordHash}'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get(self,id):
        with UserReg() as db:
            user = User(*db.getUserById(id))
            if user:
                return user
            else:
                return False