from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .contacts import Contact

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('user_contact_id', required=True, type=int)
parser.add_argument('description_contact', required=True)


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
                  'user.nickname',
                  'user_contact.nickname'))})

    def delete(self, contact_id):
        abort_if_contact_not_found(contact_id)
        session = db_session.create_session()
        contact = session.query(Contact).get(contact_id)
        session.delete(contact)
        session.commit()
        return jsonify({'success': 'OK'})


class ContactsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        contacts = session.query(Contact).all()
        return jsonify({'contacts': [item.to_dict(
            only=('id',
                  'user_id',
                  'user_contact_id',
                  'user.nickname',
                  'user_contact.nickname')) for item in contacts]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        contact = Contact(
            user_id=args['user_id'],
            user_contact_id=args['user_contact_id'],
            description_contact=args['description_contact']
        )
        session.add(contact)
        session.commit()
        return jsonify({'id': contact.id})
