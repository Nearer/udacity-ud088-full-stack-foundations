from database_setup import Restaurant, DBSession

names = [
    'Crab Shack',
    'Burger Heaven',
    'Taco Palace',
    'Some Greek Food',
    'Lotsa Italian',
    'Eat Grass And Live!'
]

session = DBSession()
for name in names:
    r = Restaurant(name=name)
    session.add(r)
    session.commit()
