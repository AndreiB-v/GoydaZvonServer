from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # CHAT relations
    chat_id: orm.Mapped[Optional[int]] = orm.mapped_column(sa.ForeignKey("chats.id"))
    chat: orm.Mapped[Optional["Chat"]] = orm.relationship(back_populates="messages",
                                                          foreign_keys=[chat_id],
                                                          cascade='save-update, delete')

    # USER relations
    user_id: orm.Mapped[Optional[int]] = orm.mapped_column(sa.ForeignKey("users.id"))
    user: orm.Mapped[Optional["User"]] = orm.relationship(back_populates="messages",
                                                          foreign_keys=[user_id],
                                                          cascade='save-update, delete')

    message = sa.Column(sa.String, nullable=True)
