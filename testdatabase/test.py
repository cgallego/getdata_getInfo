# -*- coding: utf-8 -*-
"""
SQLalchemy tutorial source: http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html 
Created on Thu Mar 20 11:54:10 2014

@author: windows
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

# Create the ORM’s “handle” to the database: the Session. 
Session = sessionmaker()
Session.configure(bind=engine)  # once engine is available
session = Session() #instantiate a Session

#  created a users table in our database, with four columns.
# The Table object is a member of a larger collection known as MetaData.
class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     password = Column(String)

     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)

#Create an Instance of the Mapped Class
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
ed_user

Base.metadata.create_all(engine) 



#////////////////////////////////////////////////////////////////////////////
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
#To persist our User object, we add() it to our Session:
session.add(ed_user)
# create a new Query object which loads instances of User. We “filter by” the name attribute of ed, 
# and indicate that we’d like only the first result in the full list of rows. A User instance is returned which is equivalent to that which we’ve added:
our_user = session.query(User).filter_by(name='ed').first() 
print our_user

#We can add more User objects at once using add_all():
session.add_all([
     User(name='wendy', fullname='Wendy Williams', password='foobar'),
     User(name='mary', fullname='Mary Contrary', password='xxg527'),
     User(name='fred', fullname='Fred Flinstone', password='blah')])

#tell the Session that we’d like to issue all remaining changes to the database and commit the transaction, which has been in progress throughout. We do this via commit():
session.commit()

## Rolling Back
# Since the Session works within a transaction, we can roll back changes made too. 
fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
session.add(fake_user)
session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all() 
#Rolling back, fake_user has been kicked out of the session:
session.rollback()
fake_user in session

###### Querying
# A Query object is created using the query() method on Session.
for instance in session.query(User).order_by(User.id): 
    print instance.name, instance.fullname
    
###### Relatioships  
#one to many association from the users to a new table which stores email addresses, which we will call addresses.   
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Address(Base):
     __tablename__ = 'addresses'
     id = Column(Integer, primary_key=True)
     email_address = Column(String, nullable=False)
     user_id = Column(Integer, ForeignKey('users.id'))
     # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
     
     user = relationship("User", backref=backref('addresses', order_by=id))

     def __repr__(self):
         return "<Address(email_address='%s')>" % self.email_address

# create the addresses table in the database, so we will issue another CREATE from our metadata, which will skip over tables which have already been created
Base.metadata.create_all(engine)          

#The two complementing relationships Address.user and User.addresses are referred to as a bidirectional relationship, and is a key feature of the SQLAlchemy ORM.         
jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses = [
                 Address(email_address='jack@google.com'),
                 Address(email_address='j25@yahoo.com')]   
jack.addresses   
        
# When using a bidirectional relationship, elements added in one direction automatically become visible in the other direction.
jack.addresses[1].user
         

###### Joins
# To construct a simple implicit join between User and Address, we can use Query.filter() to equate their related columns together
for u, a in session.query(User, Address).\
                     filter(User.id==Address.user_id).\
                     filter(Address.email_address=='jack@google.com').\
                     all():   
    print u
    print a            
         
# The actual SQL JOIN syntax, on the other hand, is most easily achieved using the Query.join() method:         
session.query(User).join(Address).\
         filter(Address.email_address=='jack@google.com').\
         all()         