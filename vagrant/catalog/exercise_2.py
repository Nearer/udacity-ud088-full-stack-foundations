from datetime import timedelta, datetime

from header import DBSession
from models import Puppy, Shelter

session = DBSession()

print "Query 1: Query all of the puppies and return the results in ascending alphabetical order\n"
for puppy in session.query(Puppy).order_by(Puppy.name):
    print puppy, puppy.name, puppy.id

print "\nQuery 2. Query all of the puppies that are less than 6 months old organized by the youngest first"
print "6-month mark is {}\n".format((datetime.now() - timedelta(weeks=24)).strftime("%c"))
for puppy in session.query(Puppy).filter(
                Puppy.dateOfBirth < (datetime.now() - timedelta(weeks=24))
).order_by(Puppy.dateOfBirth.asc()):
    print puppy.name, puppy.dateOfBirth

print "\nQuery 3. Query all puppies by ascending weight\n"
for puppy in session.query(Puppy).order_by(Puppy.weight.asc()):
    print puppy.name, round(puppy.weight, 2)

print "\nQuery 4. Query all puppies grouped by the shelter in which they are staying\n"
for puppy in session.query(Puppy).join(Puppy.shelter) \
        .order_by(Shelter.name).order_by(Puppy.name):
    print puppy.shelter.name, puppy.name
