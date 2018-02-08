from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):

    message_id = db.Column(db.Integer, primary_key=True)
    recipient_username = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Message recipient: {}, message: {}, expiration: {}>'.format(self.recipient_username,
                                                                           self.message,
                                                                           self.expiration)

def connect_to_db(app, db_uri=None):

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///messages'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def example_data():

    msg1 = Message(recipient_username='paul',
                  message='Test Message',
                  expiration=datetime(2018, 1, 12, 7, 6, 5))
    msg2 = Message(recipient_username='whitney',
                  message='Hello Whitney',
                  expiration=datetime(2018, 2, 10, 10, 6, 5))
    msg3 = Message(recipient_username='whitney',
                  message='Second message',
                  expiration=datetime(2018, 12, 5, 7, 6, 5))

    db.session.add_all([msg1, msg2, msg3])

    db.session.commit()


if __name__ == '__main__':
    from api import app
    connect_to_db(app)
    db.create_all()