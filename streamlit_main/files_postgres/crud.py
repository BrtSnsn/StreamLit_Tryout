from sqlalchemy import create_engine
from files_postgres.config import db_string
from files_postgres.models import Base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# informatie
# https://launchschool.com/books/sql_first_edition/read/multi_tables

# ont to one relationship sqlaclhemy
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-one

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_database():
    Base.metadata.create_all(engine)

# Example data load from tutorial
# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
# book = Bookz(
#     title='Deep Learning',
#     author='Ian Goodfellow',
#     pages=775,
#     published=datetime(2016, 11, 18, 12, 5, 12)
# )


if __name__ == '__main__':
    # recreate_database()
    # with session_scope() as s:        
    #     s.add(book)
    #     s.commit()
    #     s.close()
    #     print(s.query(Bookz).all())
    #     s.close()
    # a = pd.read_sql_query('select * from books', con=engine)

    create_database()
    # a = pd.read_sql_query('select * from orac_scrap_be', con=engine)
    # print(a)