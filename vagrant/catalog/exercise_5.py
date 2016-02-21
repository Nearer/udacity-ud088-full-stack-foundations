from sqlalchemy.orm import subqueryload

from models import DBSession, Shelter, Puppy


def has_room(s):
    return s.current_occupancy < s.maximum_capacity


def try_check_in(shelter, puppy):
    if has_room(shelter):
        return True, puppy, shelter
    else:
        print('\nShelter {} is full, cannot accept puppy {}.'
              .format(shelter.name, puppy.name))
        alt_shelters = [
            x for x in (
                s for s in session.query(Shelter)
                .options(subqueryload(Shelter.puppies))
                .filter(Shelter.city == shelter.city)
                .all()
            ) if has_room(x) and x.id != shelter.id
            ]
        return False, puppy, alt_shelters


def check_in(shelter, puppies):
    s = shelter
    for p in puppies:
        checked_in, p, s = try_check_in(s, p)
        if checked_in:
            p.shelter_id = s.id
            session.add_all([p, s])
            session.commit()
            print('Shelter {} has accepted puppy {}.'.format(s.name, p.name))
        else:
            if len(s) > 0:
                print('These local shelters have room:')
                for open_shelter in s:
                    print(open_shelter)
                break
            else:
                print('There are no available shelters. Open a new one.')
                break


session = DBSession()

for s in session.query(Shelter).all():
    del s.puppies[:]
    s.maximum_capacity = 5

session.commit()

puppies = session.query(Puppy)[:6]

first_shelter = session.query(Shelter) \
    .filter(Shelter.name == 'San Francisco SPCA Mission Adoption Center') \
    .first()

print('Shelter is empty:')
print(repr(first_shelter) + '\n')

check_in(first_shelter, puppies)

second_shelter = session.query(Shelter).get(3)

puppies = session.query(Puppy)[6:12]

check_in(second_shelter, puppies)
