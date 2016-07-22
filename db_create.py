# -*- coding: utf-8 -*-
from app import db
from models import Posts
from models import User
from models import Comments

# create db
db.create_all()

# insert data


# commit changes
db.session.commit()
