from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .messages import Message

parser = reqparse.RequestParser()
parser.add_argument('chat_id', required=True, type=int)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('message', required=True)


def abort_if_message_not_found(message_id):
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if not message:
        abort(404, message=f"Message {message_id} not found")


class MessageResource(Resource):
    def get(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        return jsonify({'message': message.to_dict(
            only=('id',
                  'chat_id',
                  'user_id',
                  'user.nickname',
                  'message'))})

    def delete(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        session.delete(message)
        session.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        messages = session.query(Message).all()
        return jsonify({'messages': [item.to_dict(
            only=('id',
                  'chat_id',
                  'user_id',
                  'user.nickname',
                  'message')) for item in messages]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        message = Message(
            chat_id=args['chat_id'],
            user_id=args['user_id'],
            message=args['message']
        )
        session.add(message)
        session.commit()
        return jsonify({'id': message.id})
