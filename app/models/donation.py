from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import PDPreBase


class Donation(PDPreBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
