from mongoengine import *
import datetime
import bcrypt

class Clinicians(Document):
    first_name = StringField()
    last_name = StringField()
    email = EmailField(required=True)
    password = StringField()
    roles = StringField()
    created_at = DateTimeField(default=datetime.datetime.now())

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def validate_login(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        return {
            'id':str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'roles': self.roles,
            'created_at': str(self.created_at)
        }
