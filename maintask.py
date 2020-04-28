from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgres:///data', echo=True)
Base1 = declarative_base()


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


class User(Base1):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    email = Column(String)
    password = Column(String)


metadata = MetaData
Base1.metadata.create_all(engine)


class Notes(Base1):

    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    note = Column(String, nullable=False)
    timer = Column(String)  # надо будет исправить на DataTime
    user_id = Column(ForeignKey('user.id'))

    user = relationship('User', back_populates='notes')


User.notes = relationship('Notes', order_by=Notes.id, back_populates='user')


Base1.metadata.create_all(engine)


def registration():
    log = input('введите логин: ')
    mail = input('введите мыло: ')
    pas = input('введите пароль: ')

    user = User(login=log, email=mail, password=pas)
    ses = sessionmaker(bind=engine)
    ses = ses()
    ses.add(user)
    ses.commit()


def visual():  # выводит всех юзеров
    ses = sessionmaker(bind=engine)
    ses = ses()

    for user in ses.query(User).order_by(User.id):
        print('-' * 18)
        print(f'{user.id} \n{user.login} \n{user.email} \n{user.password}')


def sign_in():
    ses = sessionmaker(bind=engine)
    ses = ses()

    login = input('введите логин: ')
    password = input('введите пароль: ')

    for user in ses.query(User).order_by(User.id):
        if login in user.login:
            if password in user.password:
                return user.id

    else:
        return False


def read_note(user_id):
    ses = sessionmaker(bind=engine)
    ses = ses()

    for note in ses.query(Notes).order_by(Notes.id):
        if note.user_id == int(user_id):
            print('-' * 18)
            print(f'id: {note.id}\nuser id: {note.user_id}\nname: {note.name}note: {note.note}')


def add_note(user_id):
    note_name = input('введите имя заметки: ')
    text = input()
    timer = input('введите время напоминания в формате 12:00 (или оставь пустым): ')

    note = Notes(user_id=user_id, name=note_name, note=text, timer=timer)

    ses = sessionmaker(bind=engine)
    ses = ses()
    ses.add(note)
    ses.commit()


def session():
    check_log = input('sign in / reg')
    if check_log == 'sign in':
        user_check = sign_in()

        while True:
            act = int(input('добавить запись(1), посмотреть записи(2), закончить работу(3)'))

            if act == 1:
                add_note(user_check)

            elif act == 2:
                read_note(user_check)

            elif act == 3:
                break

    elif check_log == 'reg':
        registration()
        session()

    else:
        print('ты что то путаешь')
        session()


if __name__ == 'main':
    registration()
    session()
