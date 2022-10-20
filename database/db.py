from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from uploads.file_handler import get_presigned_file_url

engine = create_engine("sqlite:///flask.db", echo=True, future=True)
Base = declarative_base()
session = Session(engine)


def create_db():
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    provided_file_name = Column(String)
    stored_file_name = Column(String)

    def get_profile_picture_url(self):
        return get_presigned_file_url(self.stored_file_name, self.provided_file_name)

def get_all_users():
    session = Session(engine)
    stmt = select(User)
    return session.scalars(stmt)


def create_user(name):
    with Session(engine) as session:
        user = User(name=name)
        session.add(user)
        session.commit()


def set_user_profile_picture_file_names(user_id, stored_file_name, provided_file_name):
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    user.provided_file_name = provided_file_name
    user.stored_file_name = stored_file_name
    session.commit()

