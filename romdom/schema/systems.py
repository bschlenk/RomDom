from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class SystemTable(Base):
	__tablename__ = 'systems'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	website = Column(String)
	uricomponent = Column(String)

	def __repr__(self):
		return '<System %s (%s)>' % (self.name, self.website)
