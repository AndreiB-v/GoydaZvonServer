from typing import List

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Mapped
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'chats'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # USER relations
    user_id1 = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user_id2 = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    user_1 = orm.relationship("User", foreign_keys=[user_id1])
    user_2 = orm.relationship("User", foreign_keys=[user_id2])

    # MESSAGE relations
    messages: Mapped[List["Message"]] = orm.relationship(back_populates="chat",
                                                         lazy='joined',
                                                         foreign_keys='[Message.chat_id]')
