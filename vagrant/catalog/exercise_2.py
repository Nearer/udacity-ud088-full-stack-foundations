from database_setup import Shelter, Puppy
from puppy_populator import session
from datetime import timedelta, datetime

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
