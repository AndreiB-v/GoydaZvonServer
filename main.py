from flask import Flask, render_template
from flask_restful import Api

from data import db_session
from data.__all_models import *
from data.users_resources import UserResource, UsersListResource
from data.chats_resources import ChatResource, ChatsListResource
from data.messages_resources import MessageResource, MessagesListResource
from data.contacts_resources import ContactResource, ContactsListResource

app = Flask(__name__)
api = Api(app)
app.config.from_object('config.Config')

# USERS API
api.add_resource(UsersListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

# CHATS API
api.add_resource(ChatsListResource, '/api/chats')
api.add_resource(ChatResource, '/api/chats/<int:chat_id>')

# MESSAGES API
api.add_resource(MessagesListResource, '/api/messages')
api.add_resource(MessageResource, '/api/messages/<int:message_id>')

# CONTACTS API
api.add_resource(ContactsListResource, '/api/contacts')
api.add_resource(ContactResource, '/api/contacts/<int:contact_id>')


def main():
    db_session.global_init("db/qt_project.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return render_template("index.html", users=users)


if __name__ == '__main__':
    main()
