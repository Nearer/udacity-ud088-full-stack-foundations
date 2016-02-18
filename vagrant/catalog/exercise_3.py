from models import Puppy, Profile, Adopter, DBSession

session = DBSession()

print('Puppies can have a profile:\n')

pup1 = Puppy(name='Rover-Test', gender='male')

print(pup1.name, pup1.profile.picture)

pup2 = Puppy(name='Fluffy-Test', gender='female')

print(pup2.name, pup2.profile.picture)

print('We can have a many-to-many relationship with puppies and adopters:\n')

person1, person2 = Adopter(name='Bob-Test'), Adopter(name='Sue-Test')

print('Adopters are person1 ({}) and person2 ({})'.format(person1.name, person2.name))

print('len(person1.puppies) = {}, len(person2).puppies = {}'.format(len(person1.puppies),
                                                                    len(person2.puppies)))

print('Both persons are adopting dogs {} and {}'.format(pup1.name, pup2.name))

puplist = [pup1, pup2]

person1.puppies = puplist
person2.puppies = puplist

session.add(person1)
session.add(person2)
session.commit()

person1 = session.query(Adopter).filter(Adopter.id == person1.id).first()

print('{}.puppies after query are {}'.format(person1.name, [p.name for p in person1.puppies]))

person2 = session.query(Adopter).filter(Adopter.id == person2.id).first()

print('{}.puppies after query are {}'.format(person2.name, [p.name for p in person1.puppies]))

pup1 = session.query(Puppy).filter(Puppy.id == 1).one()

pup2 = session.query(Puppy).filter(Puppy.id == 2).one()

print('{}.adopters after query are {}'.format(pup1.name, [p.name for p in pup1.adopters]))
print('{}.adopters after query are {}'.format(pup2.name, [p.name for p in pup2.adopters]))
