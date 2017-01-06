import code
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()

class CRUD():
    def save(self):
        #code.interact(local=dict(globals(), **locals()))    
        if self.id:
            db_session.add(self)
        return db_session.commit()

    def create(self):
        if not self.id:
            db_session.add(self)
        return db_session.commit()

    def destroy(self):
          db_session.delete(self)
          return db_session.commit()

class TodoList(Base, CRUD):
    __tablename__ = 'todo_list'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class TodoItem(Base, CRUD):
    __tablename__ = 'todo_item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    todo_list_id = Column(Integer, ForeignKey('todo_list.id'))
    todo_list = relationship(
        TodoList,
        backref=backref('todos',
            uselist=True,
            cascade='delete,all'
        )
    )