from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Item, User
 
engine = create_engine('sqlite:///itemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(name="navjot singh", email="navjot.chakal@yahoo.com", picture='http://www.rtjsjg.com/data/out/128/5455073-navjot-singh-sidhu-wallpapers.jpg')
session.add(user1)
session.commit()

category1 =Category(user_id=1,name = "category1")

session.add(category1)
session.commit()

item1 = Item(user_id=1,name = "abc", description = "abcdefghijklabcdefghijklabcdefghijklabcdefghijkl ", price = "$2.99",category=category1)
session.add(item1)
session.commit()


item2 = Item(user_id=1,name = "abcdef", description = "***abcdefghijklabcdefghijklabcdefghijklabcdefghijkl ", price = "$2",category=category1)
session.add(item2)
session.commit()


category2 =Category(user_id=1,name = "category2")
session.add(category2)
session.commit()
item3 = Item(user_id=1,name = "abcdef", description = "defabcdefghijklabcdefghijklabcdefghijklabcdefghijkl ", price = "$1.99",category=category2)
session.add(item3)
session.commit()
item4 = Item(user_id=1,name = "defdefabcdef", description = "def***abcdefghijklabcdefghijklabcdefghijklabcdefghijkl ", price = "$1",category=category2)
session.add(item4)
session.commit()

category3 =Category(user_id=1,name = "category3")
session.add(category3)
session.commit()

item5 = Item(user_id=1,name = "xzxzabcdef", description = "xzxzdefabcdefghijklabcdefghijklabcdefghijklabcdefghijkl ", price = "$0.99",category=category3)
session.add(item5)
session.commit()


item6 = Item(user_id=1,name = "wewedefdefabcdef", description = "wewedef***abcdefghijklabcdefghijklabcdefghijklabcdefghijkl ", price = "$1.09",category=category3)
session.add(item6)
session.commit()


print "added menu items!"

