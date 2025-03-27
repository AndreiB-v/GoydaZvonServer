from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Contact(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'contacts'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # USER relations
    user_id: orm.Mapped[Optional[int]] = orm.mapped_column(sa.ForeignKey("users.id"))
    user: orm.Mapped[Optional["User"]] = orm.relationship(back_populates="contacts",
                                                          foreign_keys=[user_id],
                                                          cascade='save-update, delete')

    # USER relations
    user_contact_id: orm.Mapped[Optional[int]] = orm.mapped_column(sa.ForeignKey("users.id"))
    user_contact: orm.Mapped[Optional["User"]] = orm.relationship(back_populates="in_whose_contacts",
                                                                  foreign_keys=[user_contact_id],
                                                                  cascade='save-update, delete')

    description_contact = sa.Column(sa.String, nullable=True)
