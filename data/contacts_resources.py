from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .contacts import Contact

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=False, type=int)
parser.add_argument('user_contact_id', required=False, type=int)
parser.add_argument('description_contact', required=False)


def abort_if_contact_not_found(contact_id):
    session = db_session.create_session()
    contact = session.query(Contact).get(contact_id)
    if not contact:
        abort(404, message=f"Contact {contact_id} not found")


class ContactResource(Resource):
    def get(self, contact_id):
        abort_if_contact_not_found(contact_id)
        session = db_session.create_session()
        contact = session.query(Contact).get(contact_id)
        return jsonify({'contact': contact.to_dict(
            only=('id',
                  'user_id',
                  'user_contact_id',
                  'description_contact'))})

    def delete(self, contact_id):
        abort_if_contact_not_found(contact_id)
        session = db_session.create_session()
        contact = session.query(Contact).get(contact_id)
        session.delete(contact)
        session.commit()
        return jsonify({'success': 'OK'})


class ContactsDescriptions(Resource):
    def get(self):
        session = db_session.create_session()
        args = parser.parse_args()
        contact = session.query(Contact).filter(Contact.user_id == args['user_id'],
                                                Contact.user_contact_id == args['user_contact_id']).first()
        if contact:
            return jsonify({'contact': contact.to_dict(
                only=('id',
                      'user_id',
                      'user_contact_id',
                      'description_contact'))})
        abort(404, message=f"Такого контакта не существует!")

    def put(self):
        session = db_session.create_session()
        args = parser.parse_args()
        contact = session.query(Contact).filter(Contact.user_id == args['user_id'],
                                                Contact.user_contact_id == args['user_contact_id']).first()
        if contact:
            contact.description_contact = args['description_contact']
            session.commit()
            return jsonify({'message': 'OK'})
        abort(404, message=f"Обязательно нужно указать user_id, user_contact_id")


class ContactsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        contacts = session.query(Contact).all()
        return jsonify({'contacts': [item.to_dict(
            only=('id',
                  'user_id',
                  'user_contact_id',
                  'description_contact')) for item in contacts]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if all([args['user_id'], args['user_contact_id']]):
            contact = Contact(
                user_id=args['user_id'],
                user_contact_id=args['user_contact_id']
            )
            session.add(contact)
            session.commit()
            return jsonify({'id': contact.id})
        abort(404, message=f"Обязательно нужно указать user_id, user_contact_id")
