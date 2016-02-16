from models import DBSession, Adopter

session = DBSession()

names = ['Bob', 'Sue', 'Larry', 'John', 'Jane', 'Larry Jr.']

for name in names:
    person = Adopter(name=name)
    session.add(person)
    session.commit()
