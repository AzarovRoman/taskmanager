from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine('postgres:///data', echo=True)
Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    email = Column(String)
    password = Column(String)


class Notes(Base):

    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    note = Column(String, nullable=False)
    timer = Column(String)  # надо будет исправить на DataTime
    user_id = Column(ForeignKey('user.id'))
    user = relationship('User', back_populates='notes')


User.notes = relationship('Notes', order_by=Notes.id, back_populates='user')
