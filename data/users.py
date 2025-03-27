from typing import List

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.orm import Mapped
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nickname = sa.Column(sa.String, nullable=True)
    phone = sa.Column(sa.String, index=True, unique=True, nullable=True)
    real_name = sa.Column(sa.String, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)

    # CHAT relations
    # chats: Mapped[List["Chat"]] = orm.relationship(lazy='joined', foreign_keys='[Chat.user_id1, Chat.user_id2]')
    # chats = orm.relationship("Chat", foreign_keys=[Chat.user_id1, Chat.user_id2])
    chats = orm.relationship('Chat', lazy='joined', primaryjoin="(User.id == Chat.user_id1) | (User.id == Chat.user_id2)")

    # MESSAGE relations
    messages: Mapped[List["Message"]] = orm.relationship(back_populates="user",
                                                         lazy='joined',
                                                         foreign_keys='[Message.user_id]')

    # CONTACT relations
    contacts: Mapped[List["Contact"]] = orm.relationship(back_populates="user",
                                                         lazy='joined',
                                                         foreign_keys='[Contact.user_id]')

    # CONTACT relations
    in_whose_contacts: Mapped[List["Contact"]] = orm.relationship(back_populates="user_contact",
                                                                  lazy='joined',
                                                                  foreign_keys='[Contact.user_contact_id]')

    def __repr__(self):
        return f'<User> {self.id} {self.nickname} {self.phone}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
