from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .users import User

parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('real_name', required=True)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id',
                  'nickname',
                  'phone',
                  'real_name',
                  'chats.id',
                  'messages.id',
                  'contacts.id',
                  'in_whose_contacts.id'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id',
                  'nickname',
                  'phone',
                  'real_name',
                  'chats.id',
                  'messages.id',
                  'contacts.id',
                  'in_whose_contacts.id')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            nickname=args['nickname'],
            phone=args['phone'],
            real_name=args['real_name']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
