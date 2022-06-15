from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Bookz(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(DateTime)
    
    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', pages={self.pages}, published={self.published}, {self.id})>"

class Scrap(Base):
    __tablename__ = 'orac_scrap_be'
    id = Column(Integer, primary_key=True)
    line = Column(String)
    amount = Column(Integer)
    reason = Column(String)
    opmerking = Column(String)
    timestamp = Column(DateTime)
    foto = Column(String)
    
    def __repr__(self):
        return f"<orac_scrap_be({self.id},line={self.line}, amount={self.amount}, reason={self.reason}, opmerking={self.opmerking})>"