from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db, Message
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

class Chats(Resource):

    def post(self):

        try:
            username = request.form.get('username').strip()
            text = request.form.get('text').strip()
            timeout = int(request.form.get('timeout').strip())
            current_time = datetime.now()
            expiration = current_time + timedelta(seconds=timeout)

        except AttributeError:
            return {}, 400

        message = Message(recipient_username=username,
                          message=text,
                          expiration=expiration)

        db.session.add(message)
        db.session.flush()
        db.session.commit()

        return { 'id': message.message_id }, 201

    def get(self, message_id=None):

        message = Message.query.get(message_id)

        if message is None:
            return {}, 404

        expiration = format_expiration_datetime(message.expiration)

        return { 'username': message.recipient_username,
                 'text': message.message,
                 'expiration_date': expiration}

api.add_resource(Chats, '/chat', '/chat/<message_id>', '/chats/<username>')


def format_expiration_datetime(datetime_obj):

    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    app.run(debug=True, host='0.0.0.0')