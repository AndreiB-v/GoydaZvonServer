from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .users import User

add_parser = reqparse.RequestParser()
add_parser.add_argument('nickname', required=False)
add_parser.add_argument('phone', required=False)
add_parser.add_argument('real_name', required=False)
add_parser.add_argument('password', required=False)

login_parser = reqparse.RequestParser()
login_parser.add_argument('phone', required=True)
login_parser.add_argument('password', required=True)

order = reqparse.RequestParser()
order.add_argument('id', required=True)
order.add_argument('text', required=True)
order.add_argument('order', required=True)


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
                  'chats.user_id1',
                  'chats.user_id2',
                  'messages.id',
                  'contacts.description_contact',
                  'contacts.user_contact.id',
                  'contacts.user_contact.real_name',
                  'contacts.user_contact.nickname',
                  'contacts.user_contact.phone',
                  'in_whose_contacts.id'))})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = add_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if args['nickname']:
            user.nickname = args['nickname']
        if args['phone']:
            user.phone = args['phone']
        if args['real_name']:
            user.real_name = args['real_name']
        if args['password']:
            user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserPhone(Resource):
    def get(self, phone):
        session = db_session.create_session()
        user = session.query(User).filter(User.phone == phone).first()
        if user:
            return jsonify({'user': user.to_dict(
                only=('id',
                      'nickname',
                      'phone',
                      'real_name',
                      'chats.id',
                      'chats.user_id1',
                      'chats.user_id2',
                      'messages.id',
                      'contacts.description_contact',
                      'contacts.user_contact.id',
                      'contacts.user_contact.real_name',
                      'contacts.user_contact.nickname',
                      'contacts.user_contact.phone',
                      'in_whose_contacts.id'))})
        abort(404, message=f"User with number {phone} not found")


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
                  'chats.user_id1',
                  'chats.user_id2',
                  'messages.id',
                  'contacts.description_contact',
                  'contacts.user_contact.id',
                  'contacts.user_contact.real_name',
                  'contacts.user_contact.nickname',
                  'contacts.user_contact.phone',
                  'in_whose_contacts.id')) for item in users]})

    def post(self):
        args = add_parser.parse_args()
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


class UserLogin(Resource):
    def get(self):
        args = login_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.phone == args['phone']).first()
        print(user)
        if user.check_password(args['password']):
            return jsonify({'message': 'OK', 'id': user.id})
        abort(404, message=f"Неверный пароль или телефон!")
