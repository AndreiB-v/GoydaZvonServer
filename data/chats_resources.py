from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .chats import Chat

parser = reqparse.RequestParser()
parser.add_argument('user_id1', required=True, type=int)
parser.add_argument('user_id2', required=True, type=int)


def abort_if_chat_not_found(chat_id):
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    if not chat:
        abort(404, message=f"Chat {chat_id} not found")


class ChatResource(Resource):
    def get(self, chat_id):
        abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        chat = session.query(Chat).get(chat_id)
        return jsonify({'chat': chat.to_dict(
            only=('id',
                  'user_id1',
                  'user_id2',
                  'user_1.nickname',
                  'user_2.nickname',
                  'messages.id'))})

    def delete(self, chat_id):
        abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        chat = session.query(Chat).get(chat_id)
        session.delete(chat)
        session.commit()
        return jsonify({'success': 'OK'})


class ChatsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        chats = session.query(Chat).all()
        return jsonify({'chats': [item.to_dict(
            only=('id',
                  'user_id1',
                  'user_id2',
                  'user_1.nickname',
                  'user_2.nickname',
                  'messages.id')) for item in chats]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        chat = Chat(
            user_id1=args['user_id1'],
            user_id2=args['user_id2']
        )
        session.add(chat)
        session.commit()
        return jsonify({'id': chat.id})
