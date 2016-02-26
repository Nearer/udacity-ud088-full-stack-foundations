import random

from database_setup import DBSession, MenuItem

session = DBSession()

items = [
    'Burger',
    'Fries',
    'Ice Cream Cone',
    'Chicken Sandwich',
    'Salad',
    'Onion Rings',
    'Soft Drink'
]

description_list = """Bacon ipsum dolor amet tri-tip spare ribs kevin strip steak, andouille beef ribs corned beef pastrami shank pork porchetta tail turducken sirloin. Kielbasa meatball short ribs hamburger jerky flank, shoulder chuck. Ground round venison boudin pork belly brisket. Drumstick ball tip ground round doner, landjaeger sausage pork chop venison chicken jowl hamburger. Sausage brisket pork, ham jowl ribeye alcatra. Ribeye jowl flank, ham hock tail fatback boudin ball tip shoulder drumstick shankle andouille. Swine shoulder leberkas, brisket ribeye tail pork chop tongue fatback cupim.
Ground round pork belly shankle frankfurter, ball tip meatball cow. Brisket salami porchetta ground round pig hamburger short ribs ball tip shank. Shankle venison pork belly shank. Beef rump kevin biltong meatloaf andouille capicola bacon. Shankle rump kevin drumstick cow.
Shankle drumstick landjaeger pork loin shoulder ribeye swine. Swine boudin jowl ball tip prosciutto bresaola flank bacon. Rump flank ground round swine cupim. Chuck drumstick frankfurter pork chop, hamburger meatloaf meatball cupim pastrami salami turkey bresaola tri-tip. Tri-tip turkey bresaola brisket strip steak sausage short ribs pastrami beef venison. Pancetta frankfurter pork loin, shank short ribs short loin brisket sirloin meatball tail shankle pastrami. Rump capicola meatball ham hock beef ham t-bone tongue turducken bresaola doner andouille.
Sausage jerky ground round short loin. Brisket kevin strip steak hamburger. Turducken jerky pastrami, leberkas bresaola picanha drumstick porchetta ground round beef. Rump alcatra meatball fatback strip steak ribeye. Cow tongue biltong brisket, alcatra andouille frankfurter shankle bresaola bacon sausage corned beef pork venison.
Filet mignon tongue ham, landjaeger pastrami jowl meatloaf pork belly. Short loin chuck swine pork chop. Cupim andouille spare ribs doner shank pork meatball, pancetta ribeye short loin pork loin turducken tri-tip tongue. Ham hock meatloaf short loin prosciutto, ham turducken short ribs beef pork chop jowl cow pancetta bresaola venison turkey. Tri-tip landjaeger alcatra chicken cupim. Boudin jowl doner, pastrami porchetta turkey ham hock. Beef ribs leberkas ham hock pork chop, spare ribs meatball boudin.""".split(
    '\n')

for item in items:
    m = MenuItem(
        name=item,
        description=random.choice(description_list),
        price=round(random.uniform(1.0, 5.0), 2)
    )
    session.add(m)

session.commit()
